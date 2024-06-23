import logging
import os
from contextlib import asynccontextmanager

import aio_pika
import aioredis
import sentry_sdk
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")

SENTRY_DSN = os.getenv("SENTRY_DSN")
REDIS_URL = os.getenv("REDIS_URL")
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0)

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
app.add_middleware(SentryAsgiMiddleware)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rabbitmq = await connect_rabbitmq()
    app.state.redis = await connect_redis()
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
    yield
    await app.state.rabbitmq.close()
    await app.state.redis.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

router = APIRouter()


@router.get("/")
async def read_root():
    logging.debug("Root endpoint accessed")
    return {"Hello": "User Service"}


app.include_router(router, tags=["users"])


async def connect_rabbitmq():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return connection


async def connect_redis():
    redis = await aioredis.from_url(REDIS_URL)
    return redis


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
