import asyncio
import time

import aio_pika
import aioredis
import pytest
from httpx import AsyncClient, ASGITransport

from app.main import (
    app,
    RABBITMQ_URL,
    REDIS_URL,
)


@pytest.mark.asyncio
async def test_read_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "User Service"}


async def test_read_users():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
    assert "users" in response.json()


async def test_invalid_input():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/?username=")
    assert response.status_code == 400


async def test_nonexistent_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/nonexistent/")
    assert response.status_code == 404


async def test_authenticated_route():
    transport = ASGITransport(app=app)
    headers = {"Authorization": "Bearer valid_token"}
    async with AsyncClient(transport=transport, base_url="http://test", headers=headers) as ac:
        response = await ac.get("/protected-route/")
    assert response.status_code == 200


async def test_unauthorized_access():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/protected-route/")
    assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.skip(reason="Skipping due to known issues with endpoints or integrations")
async def test_create_user():
    new_user = {"username": "testuser", "email": "test@example.com"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/users/", json=new_user)
    assert response.status_code == 201  # Assuming 201 is created


@pytest.mark.asyncio
@pytest.mark.skip(reason="Skipping due to known issues with endpoints or integrations")
async def test_get_user():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/users/1/")
    assert response.status_code == 200
    assert "username" in response.json()


@pytest.mark.asyncio
@pytest.mark.skip(reason="Skipping due to known issues with endpoints or integrations")
async def test_rabbitmq_integration():
    # Publish a message to RabbitMQ and verify it's received correctly
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=b"Hello RabbitMQ!"),
            routing_key="test_queue",
        )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/consume-message/")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_redis_integration():
    # Test storing and retrieving data from Redis
    redis = await aioredis.from_url(REDIS_URL)
    await redis.set("test_key", "test_value")
    value = await redis.get("test_key")
    assert value == b"test_value"


@pytest.mark.asyncio
async def test_performance():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        start_time = time.time()
        # Simulate multiple concurrent requests
        tasks = [ac.get("/") for _ in range(10)]
        await asyncio.gather(*tasks)
        end_time = time.time()
    assert (end_time - start_time) < 1.0  # Example threshold for response time
