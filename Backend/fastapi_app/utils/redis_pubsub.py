from core.redis_client import redis_client
from fastapi_socketio import SocketManager
from core.config import NOTES_CHANNEL,TAGS_CHANNEL

CHANNEL = {
    "notes": NOTES_CHANNEL,
    "tags" : TAGS_CHANNEL
}

async def publish_update(channel_name:str,data:str):
    channel = CHANNEL.get(channel_name)
    if channel:  
        await redis_client.publish(channel,data)
    else:
        print(f"Invalid channel name: {channel_name}")
        
        
async def subscribe_update(channel_name:str,socket_manager:SocketManager):
    channel = CHANNEL.get(channel_name)
    if not channel:
        print(f"Invalid channel name: {channel_name}")
        return
    pubSub = redis_client.pubsub()
    await pubSub.subscribe(channel)
    async for message in pubSub.listen():
        if message["type"] == "message":
            try:
                data = message["data"].decode("utf-8")
                await socket_manager.emit(f"{channel_name}_update",data)
            except Exception as e :
                print(f"Error processing Redis message: {e}")