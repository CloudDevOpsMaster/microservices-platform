from datetime import datetime
from typing import Dict, Any
from uuid import UUID
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EventHandler:
    """Handle incoming RabbitMQ events."""
    
    def __init__(self, create_user_use_case):
        self.create_user_use_case = create_user_use_case
    
    async def handle_event(self, message: Dict[str, Any]) -> None:
        """
        Route event to appropriate handler.
        
        Args:
            message: Event message from RabbitMQ
        """
        event_type = message.get("event_type")
        
        if event_type == "user.created":
            await self._handle_user_created(message)
        else:
            logger.warning(f"⚠️ Unknown event type: {event_type}")
    
    async def _handle_user_created(self, message: Dict[str, Any]) -> None:
        """Handle user.created event."""
        try:
            logger.info(f"🔄 Handling user.created event {message}")
            data = message.get("data", {})
            
            # Create user in User Service database
            user_data = {
                "id": data.get("id"),
                "email": data.get("email"),
                "full_name": data.get("full_name"),
                "role": data.get("role"),
                "phone": data.get("phone"),
                "department": data.get("department"),
                "is_active": data.get("is_active", True),
                "is_verified": data.get("is_verified", False),
                "created_at": data.get("created_at")
            }
            
            await self.create_user_use_case.execute_from_event(user_data)
            logger.info(f"✅ User created in User Service: {data.get('email')}")
            
        except Exception as e:
            logger.error(f"❌ Error handling user.created: {e}")
            raise