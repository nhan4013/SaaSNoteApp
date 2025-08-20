import functools
import json
from core.redis_client import redis_client
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

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
            await redis_client.set(key, json.dumps(data , default=str), ex=expire)
            return data
        return wrapper
    return decorator

def idempotency_key_required(expire=60*60*24):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Find the request object in args or kwargs
            request: Request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                request = kwargs.get("request")
            if not request:
                raise HTTPException(status_code=500, detail="Request object not found")

            idempotency_key = request.headers.get("Idempotency-Key")
            if not idempotency_key:
                raise HTTPException(status_code=400, detail="Idempotency-Key header required")

            redis_key = f"idempotency:{idempotency_key}"
            cached = await redis_client.get(redis_key)
            if cached:
                return JSONResponse(content=json.loads(cached), status_code=200)

            response = await func(*args, **kwargs)
            # Store the response in Redis
            await redis_client.set(redis_key, json.dumps(response), ex=expire)
            return response
        return wrapper
    return decorator