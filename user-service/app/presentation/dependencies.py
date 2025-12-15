# user-service/app/presentation/dependencies.py
"""
Dependency injection for FastAPI routes.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import logging

from app.infrastructure.database.connection import DatabaseConnection
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.application.use_cases.get_users_use_case import GetUsersUseCase, GetUserByIdUseCase
from app.application.use_cases.update_user_use_case import UpdateUserUseCase
from app.application.use_cases.delete_user_use_case import DeleteUserUseCase
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
security = HTTPBearer()

# Global db_connection (set from main.py)
db_connection: DatabaseConnection = None


def set_db_connection(conn: DatabaseConnection):
    """Set global database connection."""
    global db_connection
    db_connection = conn


def get_db_connection() -> DatabaseConnection:
    """Get database connection dependency."""
    if db_connection is None:
        raise RuntimeError("Database connection not initialized")
    return db_connection


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Validate JWT token locally.
    
    Args:
        credentials: Bearer token from request
        
    Returns:
        dict: User data from token
        
    Raises:
        HTTPException: If token is invalid
    """
    token = credentials.credentials
    
    try:
        # Decode and verify JWT locally
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        
        return payload
        
    except JWTError as e:
        logger.error(f"JWT validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


def get_create_user_use_case(
    db_conn: DatabaseConnection = Depends(get_db_connection)
) -> CreateUserUseCase:
    """Get CreateUserUseCase with dependencies."""
    repository = UserRepositoryImpl(db_conn)
    return CreateUserUseCase(repository)


def get_get_users_use_case(
    db_conn: DatabaseConnection = Depends(get_db_connection)
) -> GetUsersUseCase:
    """Get GetUsersUseCase with dependencies."""
    repository = UserRepositoryImpl(db_conn)
    return GetUsersUseCase(repository)


def get_get_user_by_id_use_case(
    db_conn: DatabaseConnection = Depends(get_db_connection)
) -> GetUserByIdUseCase:
    """Get GetUserByIdUseCase with dependencies."""
    repository = UserRepositoryImpl(db_conn)
    return GetUserByIdUseCase(repository)


def get_update_user_use_case(
    db_conn: DatabaseConnection = Depends(get_db_connection)
) -> UpdateUserUseCase:
    """Get UpdateUserUseCase with dependencies."""
    repository = UserRepositoryImpl(db_conn)
    return UpdateUserUseCase(repository)


def get_delete_user_use_case(
    db_conn: DatabaseConnection = Depends(get_db_connection)
) -> DeleteUserUseCase:
    """Get DeleteUserUseCase with dependencies."""
    repository = UserRepositoryImpl(db_conn)
    return DeleteUserUseCase(repository)