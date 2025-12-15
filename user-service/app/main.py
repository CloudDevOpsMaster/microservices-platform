# user-service/app/main.py
"""
User Service - Main application entry point.
"""

import asyncio
import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import get_settings
from app.infrastructure.database.connection import DatabaseConnection
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl
from app.infrastructure.messaging.rabbitmq_consumer import RabbitMQConsumer
from app.infrastructure.messaging.event_handler import EventHandler
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.presentation.routes import user_routes
from app.presentation import dependencies

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()
consumer = None
consumer_thread = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    global consumer, consumer_thread
    
    # Startup
    logger.info("Starting User Service...")
    
    # Initialize database
    db_connection = DatabaseConnection(settings.DATABASE_URL)
    await db_connection.connect()
    await db_connection.create_tables()
    
    # Inject db_connection into dependencies
    dependencies.set_db_connection(db_connection)
    
    # Initialize use case and handler for RabbitMQ events
    user_repository = UserRepositoryImpl(db_connection)
    create_user_use_case = CreateUserUseCase(user_repository)
    event_handler = EventHandler(create_user_use_case)
    
    # Get current event loop
    loop = asyncio.get_event_loop()
    
    # Start RabbitMQ consumer in background
    consumer = RabbitMQConsumer(
        queue_name="user.queue",
        callback=event_handler.handle_event
    )
    
    consumer_task = asyncio.create_task(
        asyncio.to_thread(consumer.start, loop)
    )
    yield
    
    # Shutdown
    print("Shutting down Audit Service...")
    consumer.stop()
    if consumer_task:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            pass    
    await db_connection.disconnect()
    logger.info("User Service stopped")


app = FastAPI(
    title="User Service",
    description="User management microservice",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "user-service",
        "version": "1.0.0",
        "status": "running"
    }