from datetime import datetime
from passlib.context import CryptContext
from typing import Dict, Any

from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.application.dtos.auth_dto import RegisterRequest, UserResponse
from app.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher


class RegisterUseCase:
    """Use case for user registration."""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        rabbitmq_publisher: RabbitMQPublisher
    ):
        self.user_repository = user_repository
        self.rabbitmq_publisher = rabbitmq_publisher
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def execute(self, request: RegisterRequest) -> UserResponse:
        """
        Execute user registration.
        
        Args:
            request: Registration data
            
        Returns:
            UserResponse with created user data
            
        Raises:
            ValueError: If email already exists
        """
        # Validate request
        self._validate_request(request)

        # Check if email already exists
        existing_user = await self.user_repository.find_by_email(request.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Hash password
        hashed_password = self.pwd_context.hash(request.password)
        
        # Create user entity
        user = User(
            email=request.email,
            hashed_password=hashed_password,
            full_name=request.full_name,
            role="user"
        )
        
        # Persist user
        created_user = await self.user_repository.create(user)
        
        # Publish user created event
        await self._publish_user_created_event(created_user)
        
        return UserResponse(
            id=created_user.id,
            email=created_user.email,
            full_name=created_user.full_name,
            role=created_user.role,
            is_active=created_user.is_active,
            is_verified=created_user.is_verified,
            created_at=created_user.created_at.isoformat()
        )
    
    async def _publish_user_created_event(self, user: User) -> None:
        # Publish event to RabbitMQ for User Service
        try:
            event_data = {
                "event_type": "user.created",
                "timestamp": datetime.utcnow().isoformat(),
                "data": {
                    "id": str(user.id),
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "is_active": user.is_active,
                    "is_verified": user.is_verified,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
            }
            
            self.rabbitmq_publisher.publish(
                routing_key="user.created",
                message=event_data
            )
            
        except Exception as e:
            print(f"⚠️ Failed to publish event (user already created): {e}")
            # Don't fail the request, user is already created

    def _validate_request(self, request: RegisterRequest) -> None:
        """Validate registration request."""
        if len(request.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        if len(request.full_name) < 2:
            raise ValueError("Full name must be at least 2 characters")
        
        # Validate email format (basic check)
        if "@" not in request.email or "." not in request.email:
            raise ValueError("Invalid email format")        