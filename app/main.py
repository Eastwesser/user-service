import os

import aio_pika
import aioredis
import sentry_sdk
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from app.db.session import AsyncSessionLocal
from app.routers import user

load_dotenv()

SENTRY_DSN = os.getenv("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0
)

app = FastAPI()
app.add_middleware(SentryAsgiMiddleware)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()


@app.on_event("startup")
async def startup():
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


app.include_router(user.router, prefix="/users", tags=["users"])


@app.get("/")
async def read_root():
    return {"Hello": "User Service"}


async def connect_rabbitmq():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    return connection


async def connect_redis():
    redis = await aioredis.from_url("redis://localhost")
    return redis


@app.on_event("startup")
async def startup():
    app.state.rabbitmq = await connect_rabbitmq()
    app.state.redis = await connect_redis()
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))


@app.on_event("shutdown")
async def shutdown():
    await app.state.rabbitmq.close()
    await app.state.redis.close()
    await engine.dispose()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)