from datetime import datetime
from passlib.context import CryptContext

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
        """Publish user created event to RabbitMQ."""
        event = {
            "event_type": "user.created",
            "user_id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.rabbitmq_publisher.publish("auth.events", event)