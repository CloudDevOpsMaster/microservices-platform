from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.application.dtos.user_dto import CreateUserRequest, UserResponse
from app.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher


class CreateUserUseCase:
    """Use case for creating a user."""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        rabbitmq_publisher: RabbitMQPublisher
    ):
        self.user_repository = user_repository
        self.rabbitmq_publisher = rabbitmq_publisher
    
    async def execute(self, request: CreateUserRequest) -> UserResponse:
        """
        Execute user creation.
        
        Args:
            request: User creation data
            
        Returns:
            UserResponse with created user data
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        existing_user = await self.user_repository.find_by_email(request.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        # Create user entity
        user = User(
            email=request.email,
            full_name=request.full_name,
            role=request.role,
            phone=request.phone,
            department=request.department
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
            phone=created_user.phone,
            department=created_user.department,
            created_at=created_user.created_at.isoformat(),
            updated_at=created_user.updated_at.isoformat()
        )
    
    async def _publish_user_created_event(self, user: User) -> None:
        """Publish user created event to RabbitMQ."""
        event = {
            "event_type": "user.created",
            "user_id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.rabbitmq_publisher.publish("user.events", event)