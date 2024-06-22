import asyncio

import aio_pika


async def send_message(message: str):
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("test_queue")
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue.name,
        )


async def receive_messages():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("test_queue")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body.decode())


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message("Hello, RabbitMQ!"))
    loop.run_until_complete(receive_messages())
