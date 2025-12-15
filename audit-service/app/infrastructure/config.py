from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Service
    SERVICE_NAME: str = "audit-service"
    SERVICE_PORT: int = 8003
    
    # MongoDB
    MONGODB_URL: str = "mongodb://admin:admin123@mongodb:27017"
    MONGODB_DATABASE: str = "audit_db"
    
    # RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "admin123"
    RABBITMQ_QUEUE: str = "audit.queue"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()