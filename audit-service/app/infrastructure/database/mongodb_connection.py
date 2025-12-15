from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.infrastructure.config import settings


class MongoDBConnection:
    """MongoDB connection manager."""
    
    def __init__(self):
        self.client: AsyncIOMotorClient | None = None
        self.database: AsyncIOMotorDatabase | None = None
    
    async def connect(self) -> None:
        """Establish MongoDB connection."""
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.database = self.client[settings.MONGODB_DATABASE]
        
        # Create indexes
        await self._create_indexes()
    
    async def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
    
    async def _create_indexes(self) -> None:
        """Create database indexes for performance."""
        collection = self.database.audit_logs
        
        await collection.create_index("user_id")
        await collection.create_index("resource_type")
        await collection.create_index("resource_id")
        await collection.create_index("timestamp")
        await collection.create_index([("timestamp", -1)])
    
    def get_database(self) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if self.database is None:
            raise RuntimeError("Database not connected")
        return self.database


# Global instance
mongodb_connection = MongoDBConnection()