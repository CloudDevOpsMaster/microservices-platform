# user-service/app/infrastructure/database/user_repository_impl.py
"""
SQLAlchemy implementation of User Repository.
Manages database operations for User entities.
"""
from uuid import UUID  # ✅ AGREGAR
from typing import Optional, List
from sqlalchemy import select, func, delete
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.database.models import UserModel
from app.infrastructure.database.connection import DatabaseConnection
import logging

logger = logging.getLogger(__name__)


class UserRepositoryImpl(IUserRepository):
    """SQLAlchemy implementation of User repository."""
    
    def __init__(self, db_connection: DatabaseConnection):
        """
        Initialize repository with database connection.
        
        Args:
            db_connection: DatabaseConnection instance
        """
        self.db_connection = db_connection
    
    async def create(self, user: User) -> User:
        """
        Create a new user in database.
        
        Args:
            user: User domain entity
            
        Returns:
            User: Created user entity
        """
        async with self.db_connection.get_session() as session:
            try:
                db_user = UserModel(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    role=user.role,
                    is_active=user.is_active,
                    is_verified=user.is_verified,
                    phone=user.phone,
                    department=user.department,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
                session.add(db_user)
                await session.commit()
                await session.refresh(db_user)
                logger.info(f"User created: {db_user.id}")
                return self._to_entity(db_user)
            except Exception as e:
                await session.rollback()
                logger.error(f"Error creating user: {e}")
                raise
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """
        Find user by ID.
        
        Args:
            user_id: User ID (UUID)
            
        Returns:
            Optional[User]: User entity or None
        """
        async with self.db_connection.get_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            db_user = result.scalar_one_or_none()
            return self._to_entity(db_user) if db_user else None
        
    async def find_by_email(self, email: str) -> Optional[User]:
        """
        Find user by email.
        
        Args:
            email: User email
            
        Returns:
            Optional[User]: User entity or None
        """
        async with self.db_connection.get_session() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            db_user = result.scalar_one_or_none()
            return self._to_entity(db_user) if db_user else None
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[User]: List of user entities
        """
        async with self.db_connection.get_session() as session:
            result = await session.execute(
                select(UserModel).offset(skip).limit(limit)
            )
            db_users = result.scalars().all()
            return [self._to_entity(u) for u in db_users]
    
    async def update(self, user: User) -> User:
        """
        Update existing user.
        
        Args:
            user: User domain entity with updated data
            
        Returns:
            User: Updated user entity
            
        Raises:
            ValueError: If user not found
        """
        async with self.db_connection.get_session() as session:
            try:
                result = await session.execute(
                    select(UserModel).where(UserModel.id == user.id)
                )
                db_user = result.scalar_one_or_none()
                
                if not db_user:
                    raise ValueError(f"User {user.id} not found")
                
                db_user.email = user.email
                db_user.full_name = user.full_name
                db_user.role = user.role
                db_user.is_active = user.is_active
                db_user.is_verified = user.is_verified
                db_user.phone = user.phone
                db_user.department = user.department
                db_user.updated_at = user.updated_at
                
                await session.commit()
                await session.refresh(db_user)
                logger.info(f"User updated: {db_user.id}")
                return self._to_entity(db_user)
            except Exception as e:
                await session.rollback()
                logger.error(f"Error updating user: {e}")
                raise
    
    async def delete(self, user_id: str) -> bool:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID (UUID)
            
        Returns:
            bool: True if deleted, False if not found
        """
        async with self.db_connection.get_session() as session:
            try:
                result = await session.execute(
                    select(UserModel).where(UserModel.id == user_id)
                )
                db_user = result.scalar_one_or_none()
                
                if not db_user:
                    return False
                
                await session.delete(db_user)
                await session.commit()
                logger.info(f"User deleted: {user_id}")
                return True
            except Exception as e:
                await session.rollback()
                logger.error(f"Error deleting user: {e}")
                raise
    
    async def count(self) -> int:
        """
        Count total users.
        
        Returns:
            int: Total number of users
        """
        async with self.db_connection.get_session() as session:
            result = await session.execute(select(func.count(UserModel.id)))
            return result.scalar_one()
    
    def _to_entity(self, model: UserModel) -> User:
        """
        Convert database model to domain entity.
        
        Args:
            model: UserModel instance
            
        Returns:
            User: Domain entity
        """
        return User(
            id=model.id,
            email=model.email,
            full_name=model.full_name,
            role=model.role,
            is_active=model.is_active,
            is_verified=model.is_verified,
            phone=model.phone,
            department=model.department,
            created_at=model.created_at,
            updated_at=model.updated_at
        )