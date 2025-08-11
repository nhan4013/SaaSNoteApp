from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jose import JWTError
import asyncio
import socketio
from core.redis_client import redis_client
from api.notes import notes_router as notes_router
from api.tags import tags_router as tags_router
from utils.redis_pubsub import subscribe_update
from contextlib import asynccontextmanager

sio = socketio.AsyncServer(cors_allowed_origins=["*"], async_mode='asgi')

@asynccontextmanager
async def lifespan(app: FastAPI):
    channels = ["notes","tags"]
    task = [asyncio.create_task(subscribe_update(channel,sio)) for channel in channels]
    yield
    await redis_client.close()

app = FastAPI(lifespan=lifespan)
socket_manager = socketio.ASGIApp(sio, app)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI + Socket.IO server!"}

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

@sio.event
async def connect(sid, environ):
    print(f"Socket connected: {sid}")
    await sio.emit('welcome', {'message': 'Connected to server'}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Socket disconnected: {sid}")

@sio.event
async def ping_server(sid, data):
    print(f"Received from {sid}: {data}")
    await sio.emit('pong_client', {'message': 'pong'}, to=sid)

app.include_router(notes_router)
app.include_router(tags_router)