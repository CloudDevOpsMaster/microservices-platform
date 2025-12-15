"""Get Users Use Case - Application Layer"""
from typing import List
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.application.dtos.user_dto import UserResponse, UserListResponse


class GetUsersUseCase:
    """Use case for retrieving paginated users."""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, skip: int = 0, limit: int = 100) -> UserListResponse:
        """
        Get paginated list of users.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            UserListResponse with users and pagination info
        """
        users = await self.user_repository.find_all(skip=skip, limit=limit)
        total = await self.user_repository.count()
        
        user_responses = [
            UserResponse(
                id=u.id,
                email=u.email,
                full_name=u.full_name,
                role=u.role,
                is_active=u.is_active,
                is_verified=u.is_verified,
                phone=u.phone,
                department=u.department,
                created_at=u.created_at.isoformat(),
                updated_at=u.updated_at.isoformat()
            )
            for u in users
        ]
        
        return UserListResponse(
            users=user_responses,
            total=total,
            skip=skip,
            limit=limit
        )


class GetUserByIdUseCase:
    """Use case for retrieving a single user by ID."""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str) -> UserResponse:
        """
        Get user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            UserResponse
            
        Raises:
            ValueError: If user not found
        """
        user = await self.user_repository.find_by_id(user_id)
        
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            is_verified=user.is_verified,
            phone=user.phone,
            department=user.department,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )