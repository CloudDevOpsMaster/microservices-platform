from datetime import datetime
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class AuditLog:
    """
    Domain entity for audit logs.
    Represents an immutable audit event in the system.
    """
    event_type: str
    user_id: Optional[str]
    resource_type: str
    resource_id: Optional[str]
    action: str
    metadata: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    id: Optional[str] = None
    
    def __post_init__(self):
        """Validate entity invariants."""
        if not self.event_type:
            raise ValueError("event_type cannot be empty")
        if not self.action:
            raise ValueError("action cannot be empty")
        if not self.resource_type:
            raise ValueError("resource_type cannot be empty")