from typing import Optional, List
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.database.models import UserModel


class UserRepositoryImpl(IUserRepository):
    """SQLAlchemy implementation of User repository."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        """Create a new user in database."""
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
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)
    
    async def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def find_by_email(self, email: str) -> Optional[User]:
        """Find user by email."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        db_user = result.scalar_one_or_none()
        return self._to_entity(db_user) if db_user else None
    
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        result = await self.session.execute(
            select(UserModel).offset(skip).limit(limit)
        )
        db_users = result.scalars().all()
        return [self._to_entity(u) for u in db_users]
    
    async def update(self, user: User) -> User:
        """Update existing user."""
        result = await self.session.execute(
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
        
        await self.session.commit()
        await self.session.refresh(db_user)
        return self._to_entity(db_user)
    
    async def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        db_user = result.scalar_one_or_none()
        if not db_user:
            return False
        
        await self.session.delete(db_user)
        await self.session.commit()
        return True
    
    async def count(self) -> int:
        """Count total users."""
        result = await self.session.execute(select(func.count(UserModel.id)))
        return result.scalar_one()
    
    def _to_entity(self, model: UserModel) -> User:
        """Convert database model to domain entity."""
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