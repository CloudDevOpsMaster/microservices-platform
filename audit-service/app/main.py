import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routes import audit_routes
from app.infrastructure.database.mongodb_connection import mongodb_connection
from app.infrastructure.database.mongodb_repository import MongoDBRepository
from app.infrastructure.messaging.rabbitmq_consumer import RabbitMQConsumer
from app.infrastructure.messaging.event_handler import EventHandler
from app.application.use_cases.create_audit_log_use_case import CreateAuditLogUseCase
from app.infrastructure.config import settings


consumer_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global consumer_task
    
    # Startup
    print("Starting Audit Service...")
    
    # Connect to MongoDB
    await mongodb_connection.connect()
    print("MongoDB connected")
    
    # Initialize use case and event handler
    repository = MongoDBRepository(mongodb_connection.get_database())
    use_case = CreateAuditLogUseCase(repository)
    event_handler = EventHandler(use_case)
    
    # Get current event loop
    loop = asyncio.get_event_loop()
    
    # Start RabbitMQ consumer in background
    consumer = RabbitMQConsumer(
        queue_name=settings.RABBITMQ_QUEUE,
        callback=event_handler.handle_event
    )
    
    consumer_task = asyncio.create_task(
        asyncio.to_thread(consumer.start, loop)
    )
    print(f"RabbitMQ consumer started on queue: {settings.RABBITMQ_QUEUE}")
    
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
    await mongodb_connection.disconnect()
    print("MongoDB disconnected")


app = FastAPI(
    title="Audit Service",
    description="Microservice for audit logging",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(audit_routes.router)


@app.get("/")
async def root():
    return {
        "service": "audit-service",
        "status": "running",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.SERVICE_PORT,
        reload=True
    )