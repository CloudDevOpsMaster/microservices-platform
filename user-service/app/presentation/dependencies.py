from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.infrastructure.database.database import Database
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl
from app.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.application.use_cases.get_users_use_case import GetUsersUseCase, GetUserByIdUseCase
from app.application.use_cases.update_user_use_case import UpdateUserUseCase
from app.application.use_cases.delete_user_use_case import DeleteUserUseCase
from app.core.config import settings

security = HTTPBearer()


async def get_db_session() -> AsyncSession:
    """Dependency for database session."""
    db = Database(settings.DATABASE_URL)
    async for session in db.get_session():
        yield session


def get_rabbitmq_publisher() -> RabbitMQPublisher:
    """Dependency for RabbitMQ publisher."""
    return RabbitMQPublisher(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        username=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASS
    )


async def get_current_user(
    token: Annotated[str, Depends(security)]
) -> dict:
    """Extract and validate JWT token."""
    try:
        payload = jwt.decode(
            token.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


# Use Case Dependencies
async def get_create_user_use_case(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    rabbitmq: Annotated[RabbitMQPublisher, Depends(get_rabbitmq_publisher)]
) -> CreateUserUseCase:
    """Dependency for CreateUserUseCase."""
    repository = UserRepositoryImpl(session)
    return CreateUserUseCase(repository, rabbitmq)


async def get_get_users_use_case(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> GetUsersUseCase:
    """Dependency for GetUsersUseCase."""
    repository = UserRepositoryImpl(session)
    return GetUsersUseCase(repository)


async def get_get_user_by_id_use_case(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> GetUserByIdUseCase:
    """Dependency for GetUserByIdUseCase."""
    repository = UserRepositoryImpl(session)
    return GetUserByIdUseCase(repository)


async def get_update_user_use_case(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    rabbitmq: Annotated[RabbitMQPublisher, Depends(get_rabbitmq_publisher)]
) -> UpdateUserUseCase:
    """Dependency for UpdateUserUseCase."""
    repository = UserRepositoryImpl(session)
    return UpdateUserUseCase(repository, rabbitmq)


async def get_delete_user_use_case(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    rabbitmq: Annotated[RabbitMQPublisher, Depends(get_rabbitmq_publisher)]
) -> DeleteUserUseCase:
    """Dependency for DeleteUserUseCase."""
    repository = UserRepositoryImpl(session)
    return DeleteUserUseCase(repository, rabbitmq)