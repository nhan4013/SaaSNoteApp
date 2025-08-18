import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError
import asyncio
import socketio
from core.config import SECRET_KEY,ALGORITHM
from core.redis_client import redis_client
from api.notes import notes_router as notes_router
from api.tags import tags_router as tags_router
from utils.redis_pubsub import subscribe_update
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError, ExpiredSignatureError
from prometheus_fastapi_instrumentator import Instrumentator


sio = socketio.AsyncServer(cors_allowed_origins="http://localhost:5173",async_mode='asgi')

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
    
    
Instrumentator().instrument(app).expose(app)
