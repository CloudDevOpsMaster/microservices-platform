"""Update User Use Case - Application Layer"""
from datetime import datetime
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.application.dtos.user_dto import UpdateUserRequest, UserResponse


class UpdateUserUseCase:
    """Use case for updating user information."""
    
    def __init__(
        self, 
        user_repository: IUserRepository
    ):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str, request: UpdateUserRequest) -> UserResponse:
        """
        Update user information.
        
        Args:
            user_id: User identifier
            request: UpdateUserRequest with fields to update
            
        Returns:
            UserResponse with updated user data
            
        Raises:
            ValueError: If user not found or validation fails
        """
        # Get existing user
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")
        
        # Update only provided fields
        if request.full_name is not None:
            if not request.full_name.strip():
                raise ValueError("Full name cannot be empty")
            user.full_name = request.full_name.strip()
        
        if request.phone is not None:
            user.phone = request.phone
        
        if request.department is not None:
            user.department = request.department
        
        if request.role is not None:
            if request.role not in ["user", "admin", "moderator"]:
                raise ValueError(f"Invalid role: {request.role}")
            user.role = request.role
        
        if request.is_active is not None:
            user.is_active = request.is_active
        
        # Update timestamp
        user.updated_at = datetime.utcnow()
        
        # Save changes
        updated_user = await self.user_repository.update(user)
        
        # # Publish event to RabbitMQ
        # try:
        #     event_data = {
        #         "event_type": "user.updated",
        #         "user_id": updated_user.id,
        #         "email": updated_user.email,
        #         "full_name": updated_user.full_name,
        #         "role": updated_user.role,
        #         "is_active": updated_user.is_active,
        #         "updated_at": updated_user.updated_at.isoformat()
        #     }
        #     await self.rabbitmq_publisher.publish(
        #         exchange="user_events",
        #         routing_key="user.updated",
        #         message=event_data
        #     )
        # except Exception as e:
        #     # Log error but don't fail the operation
        #     print(f"Failed to publish user.updated event: {e}")
        
        return UserResponse(
            id=updated_user.id,
            email=updated_user.email,
            full_name=updated_user.full_name,
            role=updated_user.role,
            is_active=updated_user.is_active,
            is_verified=updated_user.is_verified,
            phone=updated_user.phone,
            department=updated_user.department,
            created_at=updated_user.created_at.isoformat(),
            updated_at=updated_user.updated_at.isoformat()
        )