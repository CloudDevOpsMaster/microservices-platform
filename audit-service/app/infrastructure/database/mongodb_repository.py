from datetime import datetime
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from bson import ObjectId

from app.domain.entities.audit_log import AuditLog
from app.domain.repositories.audit_repository import IAuditRepository


class MongoDBRepository(IAuditRepository):
    """MongoDB implementation of audit repository."""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.db = database
        self.collection = self.db.audit_logs
    
    async def create(self, audit_log: AuditLog) -> AuditLog:
        """Create new audit log entry in MongoDB."""
        document = {
            "event_type": audit_log.event_type,
            "user_id": audit_log.user_id,
            "resource_type": audit_log.resource_type,
            "resource_id": audit_log.resource_id,
            "action": audit_log.action,
            "metadata": audit_log.metadata,
            "timestamp": audit_log.timestamp
        }
        
        result = await self.collection.insert_one(document)
        audit_log.id = str(result.inserted_id)
        
        return audit_log
    
    async def find_by_user(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[AuditLog]:
        """Find audit logs by user ID."""
        cursor = self.collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)
        
        logs = []
        async for doc in cursor:
            logs.append(self._document_to_entity(doc))
        
        return logs
    
    async def find_by_resource(
        self,
        resource_type: str,
        resource_id: str
    ) -> List[AuditLog]:
        """Find audit logs by resource."""
        cursor = self.collection.find({
            "resource_type": resource_type,
            "resource_id": resource_id
        }).sort("timestamp", -1)
        
        logs = []
        async for doc in cursor:
            logs.append(self._document_to_entity(doc))
        
        return logs
    
    async def find_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        limit: int = 1000
    ) -> List[AuditLog]:
        """Find audit logs within date range."""
        cursor = self.collection.find({
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }).sort("timestamp", -1).limit(limit)
        
        logs = []
        async for doc in cursor:
            logs.append(self._document_to_entity(doc))
        
        return logs
    
    def _document_to_entity(self, doc: dict) -> AuditLog:
        """Convert MongoDB document to domain entity."""
        return AuditLog(
            id=str(doc["_id"]),
            event_type=doc["event_type"],
            user_id=doc.get("user_id"),
            resource_type=doc["resource_type"],
            resource_id=doc.get("resource_id"),
            action=doc["action"],
            metadata=doc["metadata"],
            timestamp=doc["timestamp"]
        )