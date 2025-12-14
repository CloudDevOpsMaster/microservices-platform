import pytest
from app.domain.entities.user import User
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl


@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating user in database."""
    repo = UserRepositoryImpl(db_session)
    
    user = User(
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    
    result = await repo.create(user)
    
    assert result.id is not None
    assert result.email == "test@example.com"
    assert result.full_name == "Test User"


@pytest.mark.asyncio
async def test_find_by_id(db_session):
    """Test finding user by ID."""
    repo = UserRepositoryImpl(db_session)
    
    user = User(email="test@example.com", full_name="Test User")
    created = await repo.create(user)
    
    found = await repo.find_by_id(created.id)
    
    assert found is not None
    assert found.id == created.id
    assert found.email == created.email


@pytest.mark.asyncio
async def test_find_by_email(db_session):
    """Test finding user by email."""
    repo = UserRepositoryImpl(db_session)
    
    user = User(email="unique@example.com", full_name="Unique User")
    await repo.create(user)
    
    found = await repo.find_by_email("unique@example.com")
    
    assert found is not None
    assert found.email == "unique@example.com"


@pytest.mark.asyncio
async def test_find_by_email_not_found(db_session):
    """Test finding non-existent user."""
    repo = UserRepositoryImpl(db_session)
    
    found = await repo.find_by_email("nonexistent@example.com")
    
    assert found is None


@pytest.mark.asyncio
async def test_update_user(db_session):
    """Test updating user."""
    repo = UserRepositoryImpl(db_session)
    
    user = User(email="test@example.com", full_name="Original Name")
    created = await repo.create(user)
    
    created.full_name = "Updated Name"
    created.phone = "+1234567890"
    
    updated = await repo.update(created)
    
    assert updated.full_name == "Updated Name"
    assert updated.phone == "+1234567890"


@pytest.mark.asyncio
async def test_delete_user(db_session):
    """Test deleting user."""
    repo = UserRepositoryImpl(db_session)
    
    user = User(email="delete@example.com", full_name="Delete Me")
    created = await repo.create(user)
    
    result = await repo.delete(created.id)
    
    assert result is True
    
    found = await repo.find_by_id(created.id)
    assert found is None


@pytest.mark.asyncio
async def test_count_users(db_session):
    """Test counting users."""
    repo = UserRepositoryImpl(db_session)
    
    for i in range(3):
        user = User(email=f"user{i}@example.com", full_name=f"User {i}")
        await repo.create(user)
    
    count = await repo.count()
    
    assert count == 3