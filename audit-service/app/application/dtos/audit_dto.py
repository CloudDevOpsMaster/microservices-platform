from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class AuditLogResponse(BaseModel):
    """Response DTO for audit log."""
    id: str
    event_type: str
    user_id: Optional[str]
    resource_type: str
    resource_id: Optional[str]
    action: str
    metadata: Dict[str, Any]
    timestamp: str
    
    class Config:
        from_attributes = True


class AuditLogQuery(BaseModel):
    """Query parameters for audit logs."""
    user_id: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    limit: int = Field(default=100, ge=1, le=1000)