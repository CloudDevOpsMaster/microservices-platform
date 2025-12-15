from datetime import datetime
from typing import Dict, Any

from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.audit_repository import IAuditRepository
from app.application.dtos.audit_dto import AuditLogResponse


class CreateAuditLogUseCase:
    """Use case for creating audit log entries."""
    
    def __init__(self, audit_repository: IAuditRepository):
        self.audit_repository = audit_repository
    
    async def execute(
        self,
        event_type: str,
        user_id: str | None,
        resource_type: str,
        resource_id: str | None,
        action: str,
        metadata: Dict[str, Any]
    ) -> AuditLogResponse:
        """
        Create audit log entry.
        
        Args:
            event_type: Type of event (e.g., 'user.created')
            user_id: ID of user performing action
            resource_type: Type of resource (e.g., 'user')
            resource_id: ID of affected resource
            action: Action performed (e.g., 'create', 'update')
            metadata: Additional event data
            
        Returns:
            AuditLogResponse with created log
        """
        audit_log = AuditLog(
            event_type=event_type,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            metadata=metadata,
            timestamp=datetime.utcnow()
        )
        
        created_log = await self.audit_repository.create(audit_log)
        
        return AuditLogResponse(
            id=str(created_log.id),
            event_type=created_log.event_type,
            user_id=created_log.user_id,
            resource_type=created_log.resource_type,
            resource_id=created_log.resource_id,
            action=created_log.action,
            metadata=created_log.metadata,
            timestamp=created_log.timestamp.isoformat()
        )