from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://admin:admin123@localhost:5433/users_db"
    
    # RabbitMQ
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "admin"
    RABBITMQ_PASSWORD: str = "admin123"
    
    # Auth Service
    AUTH_SERVICE_URL: str = "http://localhost:8001"
    
    # JWT - Must match Auth Service
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    
    # App
    APP_NAME: str = "User Service"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()