import pytest
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

from app.domain.entities.audit_log import AuditLog
from app.infrastructure.database.mongodb_repository import MongoDBRepository


@pytest.fixture
async def repository():
    """Create test repository with in-memory MongoDB."""
    client = AsyncIOMotorClient("mongodb://admin:admin123@localhost:27017")
    db = client.test_audit_db
    repo = MongoDBRepository(db)
    
    yield repo
    
    # Cleanup
    await db.audit_logs.drop()
    client.close()


@pytest.mark.asyncio
async def test_create_audit_log(repository):
    """Test creating audit log."""
    audit_log = AuditLog(
        event_type="user.created",
        user_id="user123",
        resource_type="user",
        resource_id="user123",
        action="create",
        metadata={"email": "test@example.com"},
        timestamp=datetime.utcnow()
    )
    
    created = await repository.create(audit_log)
    
    assert created.id is not None
    assert created.event_type == "user.created"
    assert created.user_id == "user123"


@pytest.mark.asyncio
async def test_find_by_user(repository):
    """Test finding logs by user."""
    # Create multiple logs
    for i in range(3):
        log = AuditLog(
            event_type=f"action.{i}",
            user_id="user123",
            resource_type="test",
            resource_id=f"res{i}",
            action="test",
            metadata={},
            timestamp=datetime.utcnow()
        )
        await repository.create(log)
    
    logs = await repository.find_by_user("user123", limit=10)
    
    assert len(logs) == 3
    assert all(log.user_id == "user123" for log in logs)