from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.infrastructure.database.connection import DatabaseConnection
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from app.presentation.routes import auth_routes
from app.presentation.dependencies import set_infrastructure

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    logger.info("Starting Auth Service...")
    
    # Initialize database
    db_connection = DatabaseConnection(settings.DATABASE_URL)
    await db_connection.connect()
    await db_connection.create_tables()
    
    # Initialize Redis
    redis_client = RedisClient(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )
    await redis_client.connect()
    
    # Initialize RabbitMQ
    rabbitmq_publisher = RabbitMQPublisher(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        username=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD
    )
    rabbitmq_publisher.connect()
    
    # Set infrastructure in dependencies
    set_infrastructure(db_connection, redis_client, rabbitmq_publisher)
    
    logger.info("Auth Service started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Auth Service...")
    await db_connection.disconnect()
    await redis_client.disconnect()
    rabbitmq_publisher.disconnect()
    logger.info("Auth Service stopped")


# Create FastAPI app
app = FastAPI(
    title="Auth Service",
    description="Authentication and authorization microservice",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "auth-service",
        "version": "1.0.0",
        "status": "running"
    }