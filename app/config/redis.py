import os

import aioredis

REDIS_URL = os.getenv("REDIS_URL")

redis = aioredis.from_url(REDIS_URL)


async def set_value(key: str, value: str):
    await redis.set(key, value)


async def get_value(key: str):
    return await redis.get(key)
