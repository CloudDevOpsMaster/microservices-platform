from datetime import datetime
from typing import Any, Dict
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.application.dtos.user_dto import CreateUserRequest, UserResponse


class CreateUserUseCase:
    """Use case for creating users."""
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def execute(self, request: CreateUserRequest) -> UserResponse:
        """
        Create a new user (API endpoint).
        
        Args:
            request: User creation data
            
        Returns:
            UserResponse with created user data
        """
        # Check if user already exists
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            raise ValueError("User with this email already exists")
        
        # Create user entity
        user = User(
            email=request.email,
            full_name=request.full_name,
            role=request.role,
            phone=request.phone,
            department=request.department
        )
        
        # Persist
        created_user = await self.user_repository.create(user)
        
        return UserResponse.from_entity(created_user)
    
    async def execute_from_event(self, data: Dict[str, Any]) -> None:
        """
        Create user from RabbitMQ event.
        
        Args:
            data: User data from event
        """
        try:
            # Check if user already exists
            user_id = data["id"] if isinstance(data["id"], str) else data["id"]
            existing = await self.user_repository.find_by_id(user_id)
            
            if existing:
                print(f"ℹ️ User already exists: {data['email']}")
                return
            
            # Create user entity with existing ID
            user = User(
                id=user_id,
                email=data["email"],
                full_name=data["full_name"],
                role=data.get("role", "user"),
                phone=data.get("phone"),
                department=data.get("department"),
                is_active=data.get("is_active", True),
                is_verified=data.get("is_verified", False),
                created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.utcnow()
            )
            
            # Persist
            await self.user_repository.create(user)
            print(f"✅ User synced to User Service DB: {user.email}")
            
        except Exception as e:
            print(f"❌ Error creating user from event: {e}")
            raise