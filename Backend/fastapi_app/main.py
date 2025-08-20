import logging
from typing import Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError
import asyncio
import socketio
from utils.limiter import limiter
from core.config import SECRET_KEY,ALGORITHM
from core.redis_client import redis_client 
from api.notes import notes_router as notes_router
from api.tags import tags_router as tags_router
from utils.redis_pubsub import subscribe_update
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError, ExpiredSignatureError
from prometheus_fastapi_instrumentator import Instrumentator
import os
import sys
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


sio = socketio.AsyncServer(cors_allowed_origins="http://localhost:5173",async_mode='asgi')

# Create a Limiter instance, using the client's IP address as the key


@asynccontextmanager
async def lifespan(app: FastAPI):
    channels = ["notes","tags"]
    task = [asyncio.create_task(subscribe_update(channel,sio)) for channel in channels]
    yield
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return JSONResponse(
            status_code=401,
            content={"error": "Unauthorized", "detail": exc.detail}
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(JWTError)
async def jwt_exception_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Invalid token", "custom_message": "JWT error handled globally"},
    )

app.include_router(notes_router)
app.include_router(tags_router)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

socket_app = socketio.ASGIApp(sio, app)

@sio.event
async def connect(sid,environ,auth):
    token = auth.get("token") if auth else None
    if not token:
        await sio.emit("token_expired", {"detail": "No token provided"}, to=sid)
        print("No Token provided")
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"User connected: {payload}")
    except ExpiredSignatureError:
        await sio.emit("token_expired", {"detail": "Token expired"}, to=sid)
        logging.info("Token expired")
        print("Token expired")
        
    except JWTError:
        await sio.emit("token_expired", {"detail": "Invalid token"}, to=sid)
        print("Invalid token")
       


@sio.event
async def disconnect(sid):
    print(f"Socket disconnected: {sid}")

@sio.event
async def ping_server(sid, data):
    print(f"Received from {sid}: {data}")
    await sio.emit('pong_client', {'message': 'pong'}, to=sid)

# Store active users per note
active_docs: Dict[str, Dict[str, dict]] = {}

@sio.event
async def join_document(sid, data):
    note_id = data.get('noteId')
    user_info = data.get('user', {})
    if not note_id:
        return {'error': 'noteId is required'}
    await sio.enter_room(sid, f"doc:{note_id}")
    if note_id not in active_docs:
        active_docs[note_id] = {}
    active_docs[note_id][sid] = user_info
    await sio.emit('user_joined', {
        'user': user_info,
        'activeUsers': list(active_docs[note_id].values())
    }, room=f"doc:{note_id}", skip_sid=sid)
    return {'activeUsers': list(active_docs[note_id].values())}

@sio.event
async def leave_document(sid, data):
    note_id = data.get('noteId')
    if not note_id:
        return
    await sio.leave_room(sid, f"doc:{note_id}")
    if note_id in active_docs and sid in active_docs[note_id]:
        user_info = active_docs[note_id][sid]
        del active_docs[note_id][sid]
        await sio.emit('user_left', {
            'user': user_info,
            'activeUsers': list(active_docs[note_id].values())
        }, room=f"doc:{note_id}")

@sio.event
async def sync_document(sid, data):
    note_id = data.get('noteId')
    update = data.get('update')
    if not note_id or not update:
        return {'error': 'noteId and update are required'}
    # Optionally, persist update in Redis here
    await sio.emit('document_update', {
        'noteId': note_id,
        'update': update
    }, room=f"doc:{note_id}", skip_sid=sid)
    return {'success': True}

@sio.event
async def get_document(sid, data):
    note_id = data.get('noteId')
    # Optionally, fetch updates from Redis if you want persistence
    return {'noteId': note_id, 'updates': []}
        
    
Instrumentator().instrument(app).expose(app)

os.makedirs("../../logs", exist_ok=True)
try:
    import colorlog
    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)s %(name)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    stream_handler = colorlog.StreamHandler(sys.stdout)
    stream_handler.setFormatter(color_formatter)
except ImportError:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

file_handler = logging.FileHandler("../../logs/fastapi_app.log")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))


logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, stream_handler]
)

for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
    logger = logging.getLogger(logger_name)
    logger.handlers = []
    logger.propagate = True