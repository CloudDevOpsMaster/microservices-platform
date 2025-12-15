"""Delete User Use Case - Application Layer"""
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher


class DeleteUserUseCase:
    """Use case for deleting a user."""
    
    def __init__(
        self, 
        user_repository: IUserRepository,
        rabbitmq_publisher: RabbitMQPublisher
    ):
        self.user_repository = user_repository
        self.rabbitmq_publisher = rabbitmq_publisher
    
    async def execute(self, user_id: str) -> None:
        """
        Delete user by ID.
        
        Args:
            user_id: User identifier
            
        Raises:
            ValueError: If user not found
        """
        # Check if user exists and get data for event
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Store data before deletion
        user_email = user.email
        user_name = user.full_name
        
        # Delete user
        deleted = await self.user_repository.delete(user_id)
        if not deleted:
            raise ValueError(f"Failed to delete user {user_id}")
        
        # Publish event to RabbitMQ
        try:
            event_data = {
                "event_type": "user.deleted",
                "user_id": user_id,
                "email": user_email,
                "full_name": user_name
            }
            await self.rabbitmq_publisher.publish(
                exchange="user_events",
                routing_key="user.deleted",
                message=event_data
            )
        except Exception as e:
            # Log error but don't fail the operation
            print(f"Failed to publish user.deleted event: {e}")