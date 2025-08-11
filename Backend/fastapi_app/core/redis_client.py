import redis.asyncio as redis

from core.config import REDIS_URL

redis_client = redis.Redis.from_url(REDIS_URL)