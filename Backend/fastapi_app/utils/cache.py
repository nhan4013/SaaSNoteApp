import functools
import json
from core.redis_client import redis_client

def redis_cache(key_builder, expire=300):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            key = key_builder(*args, **kwargs)
            cached = await redis_client.get(key)
            if cached:
                print(cached)
                return json.loads(cached)
            result = await func(*args, **kwargs)
            if isinstance(result,list):
                data = [item.dict() for item in result]
            else:
                data = result.dict() if hasattr(result, 'dict') else result
            print("BBBBBBBBBBBB")
            await redis_client.set(key, json.dumps(data , default=str), ex=expire)
            return data
        return wrapper
    return decorator