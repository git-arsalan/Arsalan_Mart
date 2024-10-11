# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from typing import AsyncGenerator
from aiokafka import AIOKafkaConsumer
import asyncio
import aiosmtplib
from email.message import EmailMessage
import json

async def consume_messages(topic, bootstrap_servers):
    # Create a consumer instance.
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        group_id="user-reg-group",
        auto_offset_reset='earliest'
    )

    # Start the consumer.
    await consumer.start()
    try:
        # Continuously listen for messages.
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            user_data = message.value
            to_email = user_data['email']
            user_name = user_data['name']
            print(f"Sending email to {to_email}")
            await send_email(to_email, user_name)
    finally:
        # Ensure to close the consumer when done.
        await consumer.stop()


async def send_email(to_email: str, user_name: str):
    # Create the email content
    message = EmailMessage()
    message["From"] = "backuparsalan2088@gmail.com"
    message["To"] = to_email
    message["Subject"] = "Welcome to Arsalan Mart!"
    message.set_content(f"Hello {user_name},\n\nThank you for registering on Arsalan Mart!")

    # Send the email (example using Gmail's SMTP server)
    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username="backuparsalan2088@gmail.com",
        password="arsalan@2o88"
    )


# The first part of the function, before the yield, will
# be executed before the application starts.
# https://fastapi.tiangolo.com/advanced/events/#lifespan-function
# loop = asyncio.get_event_loop()
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    # print("Creating tables..")
    task = asyncio.create_task(consume_messages('user_registered', 'broker:19092'))
    yield


app = FastAPI(title="User Service",
    description="API for managing users",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "User Notification", "description": "Operations with user Notification"}
    ])


@app.get("/")
def read_root():
    return {"API Description": "User Notification Service"}

# Kafka Producer as a dependency
async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()