from typing import Dict, Any

from app.application.use_cases.create_audit_log_use_case import CreateAuditLogUseCase


class EventHandler:
    """Handles incoming events from RabbitMQ."""
    
    def __init__(self, create_audit_log_use_case: CreateAuditLogUseCase):
        self.create_audit_log_use_case = create_audit_log_use_case
    
    async def handle_event(self, event: Dict[str, Any]) -> None:
        """
        Process incoming event and create audit log.
        
        Args:
            event: Event data from RabbitMQ
        """
        event_type = event.get("event_type")
        
        if not event_type:
            print(f"Invalid event: missing event_type")
            return
        
        # Parse event based on type
        if event_type.startswith("user."):
            await self._handle_user_event(event)
        elif event_type.startswith("auth."):
            await self._handle_auth_event(event)
        else:
            await self._handle_generic_event(event)
    
    async def _handle_user_event(self, event: Dict[str, Any]) -> None:
        """Handle user-related events."""
        action = event["event_type"].split(".")[-1]  # 'created', 'updated', etc.
        
        await self.create_audit_log_use_case.execute(
            event_type=event["event_type"],
            user_id=event.get("user_id"),
            resource_type="user",
            resource_id=event.get("user_id"),
            action=action,
            metadata={
                "email": event.get("email"),
                "full_name": event.get("full_name"),
                "timestamp": event.get("timestamp"),
                **{k: v for k, v in event.items() if k not in [
                    "event_type", "user_id", "email", "full_name", "timestamp"
                ]}
            }
        )
    
    async def _handle_auth_event(self, event: Dict[str, Any]) -> None:
        """Handle authentication-related events."""
        action = event["event_type"].split(".")[-1]
        
        await self.create_audit_log_use_case.execute(
            event_type=event["event_type"],
            user_id=event.get("user_id"),
            resource_type="auth",
            resource_id=None,
            action=action,
            metadata=event
        )
    
    async def _handle_generic_event(self, event: Dict[str, Any]) -> None:
        """Handle generic events."""
        await self.create_audit_log_use_case.execute(
            event_type=event["event_type"],
            user_id=event.get("user_id"),
            resource_type="system",
            resource_id=None,
            action=event["event_type"],
            metadata=event
        )