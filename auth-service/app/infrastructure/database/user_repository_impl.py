from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.database.models import UserModel
from app.infrastructure.database.connection import DatabaseConnection


class UserRepositoryImpl(IUserRepository):
    """SQLAlchemy implementation of user repository."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
    
    async def create(self, user: User) -> User:
        """Create new user in database."""
        async with self.db_connection.get_session() as session:
            user_model = UserModel(
                id=user.id,
                email=user.email,
                hashed_password=user.hashed_password,
                full_name=user.full_name,
                is_active=user.is_active,
                is_verified=user.is_verified,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            session.add(user_model)
            await session.flush()
            return self._to_entity(user_model)
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        async with self.db_connection.get_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            user_model = result.scalar_one_or_none()
            return self._to_entity(user_model) if user_model else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        async with self.db_connection.get_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            user_model = result.scalar_one_or_none()
            return self._to_entity(user_model) if user_model else None
    
    async def update(self, user: User) -> User:
        """Update existing user."""
        async with self.db_connection.get_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user.id)
            )
            user_model = result.scalar_one_or_none()
            if not user_model:
                raise ValueError(f"User {user.id} not found")
            
            user_model.email = user.email
            user_model.hashed_password = user.hashed_password
            user_model.full_name = user.full_name
            user_model.is_active = user.is_active
            user_model.is_verified = user.is_verified
            user_model.role = user.role
            user_model.updated_at = user.updated_at
            
            await session.flush()
            return self._to_entity(user_model)
    
    async def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        async with self.db_connection.get_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            user_model = result.scalar_one_or_none()
            if user_model:
                await session.delete(user_model)
                return True
            return False
    
    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity."""
        return User(
            id=model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            is_active=model.is_active,
            is_verified=model.is_verified,
            role=model.role,
            created_at=model.created_at,
            updated_at=model.updated_at
        )