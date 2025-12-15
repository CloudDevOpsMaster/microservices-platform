from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import datetime

from app.application.dtos.audit_dto import AuditLogResponse, AuditLogQuery
from app.domain.repositories.audit_repository import IAuditRepository
from app.infrastructure.database.mongodb_repository import MongoDBRepository
from app.infrastructure.database.mongodb_connection import mongodb_connection


router = APIRouter(prefix="/audit", tags=["audit"])


def get_repository() -> IAuditRepository:
    """Dependency injection for repository."""
    return MongoDBRepository(mongodb_connection.get_database())


@router.get("/logs", response_model=List[AuditLogResponse])
async def get_audit_logs(
    user_id: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    resource_id: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    repository: IAuditRepository = Depends(get_repository)
):
    """
    Get audit logs with optional filters.
    
    Query parameters:
    - user_id: Filter by user ID
    - resource_type: Filter by resource type
    - resource_id: Filter by resource ID
    - start_date: Filter from date
    - end_date: Filter to date
    - limit: Maximum results
    """
    try:
        if user_id:
            logs = await repository.find_by_user(user_id, limit)
        elif resource_type and resource_id:
            logs = await repository.find_by_resource(resource_type, resource_id)
        elif start_date and end_date:
            logs = await repository.find_by_date_range(start_date, end_date, limit)
        else:
            raise HTTPException(
                status_code=400,
                detail="Provide user_id, resource filters, or date range"
            )
        
        return [
            AuditLogResponse(
                id=str(log.id),
                event_type=log.event_type,
                user_id=log.user_id,
                resource_type=log.resource_type,
                resource_id=log.resource_id,
                action=log.action,
                metadata=log.metadata,
                timestamp=log.timestamp.isoformat()
            )
            for log in logs
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "audit-service"}