from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

from app.domain.entities.audit_log import AuditLog


class IAuditRepository(ABC):
    """Interface for audit log persistence."""
    
    @abstractmethod
    async def create(self, audit_log: AuditLog) -> AuditLog:
        """Create new audit log entry."""
        pass
    
    @abstractmethod
    async def find_by_user(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[AuditLog]:
        """Find audit logs by user ID."""
        pass
    
    @abstractmethod
    async def find_by_resource(
        self,
        resource_type: str,
        resource_id: str
    ) -> List[AuditLog]:
        """Find audit logs by resource."""
        pass
    
    @abstractmethod
    async def find_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 1000
    ) -> List[AuditLog]:
        """Find audit logs within date range."""
        pass