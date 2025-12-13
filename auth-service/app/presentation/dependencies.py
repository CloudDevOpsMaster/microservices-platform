from functools import lru_cache
from app.config import get_settings
from app.infrastructure.database.connection import DatabaseConnection
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from app.application.use_cases.login_use_case import LoginUseCase
from app.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.application.use_cases.register_use_case import RegisterUseCase

# Global instances (initialized in main.py)
_db_connection: DatabaseConnection = None
_redis_client: RedisClient = None
_rabbitmq_publisher: RabbitMQPublisher = None


def set_infrastructure(db: DatabaseConnection, redis: RedisClient, rabbitmq: RabbitMQPublisher):
    """Set infrastructure instances."""
    global _db_connection, _redis_client, _rabbitmq_publisher
    _db_connection = db
    _redis_client = redis
    _rabbitmq_publisher = rabbitmq


def get_login_use_case() -> LoginUseCase:
    """Dependency for login use case."""
    settings = get_settings()
    user_repository = UserRepositoryImpl(_db_connection)
    return LoginUseCase(
        user_repository=user_repository,
        redis_client=_redis_client,
        rabbitmq_publisher=_rabbitmq_publisher,
        jwt_secret=settings.JWT_SECRET_KEY,
        jwt_algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )


def get_refresh_use_case() -> RefreshTokenUseCase:
    """Dependency for refresh token use case."""
    settings = get_settings()
    user_repository = UserRepositoryImpl(_db_connection)
    return RefreshTokenUseCase(
        user_repository=user_repository,
        redis_client=_redis_client,
        jwt_secret=settings.JWT_SECRET_KEY,
        jwt_algorithm=settings.JWT_ALGORITHM,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )


def get_register_use_case() -> RegisterUseCase:
    """Dependency for register use case."""
    user_repository = UserRepositoryImpl(_db_connection)
    return RegisterUseCase(
        user_repository=user_repository,
        rabbitmq_publisher=_rabbitmq_publisher
    )