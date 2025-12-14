import pytest
from unittest.mock import AsyncMock
from app.domain.entities.user import User
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.application.dtos.user_dto import CreateUserRequest


@pytest.mark.asyncio
async def test_create_user_success(mock_rabbitmq):
    """Test successful user creation."""
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.find_by_email.return_value = None
    
    created_user = User(
        id="test-123",
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    mock_repo.create.return_value = created_user
    
    use_case = CreateUserUseCase(mock_repo, mock_rabbitmq)
    request = CreateUserRequest(
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    
    # Act
    result = await use_case.execute(request)
    
    # Assert
    assert result.email == "test@example.com"
    assert result.full_name == "Test User"
    assert result.role == "user"
    assert result.id == "test-123"
    mock_repo.find_by_email.assert_called_once_with("test@example.com")
    mock_repo.create.assert_called_once()
    mock_rabbitmq.publish.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_email_exists(mock_rabbitmq):
    """Test user creation with existing email."""
    # Arrange
    mock_repo = AsyncMock()
    existing_user = User(
        id="existing-123",
        email="test@example.com",
        full_name="Existing User",
        role="user"
    )
    mock_repo.find_by_email.return_value = existing_user
    
    use_case = CreateUserUseCase(mock_repo, mock_rabbitmq)
    request = CreateUserRequest(
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="Email already registered"):
        await use_case.execute(request)
    
    mock_repo.find_by_email.assert_called_once()
    mock_repo.create.assert_not_called()
    mock_rabbitmq.publish.assert_not_called()


@pytest.mark.asyncio
async def test_create_user_with_optional_fields(mock_rabbitmq):
    """Test user creation with phone and department."""
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.find_by_email.return_value = None
    
    created_user = User(
        id="test-456",
        email="admin@example.com",
        full_name="Admin User",
        role="admin",
        phone="+1234567890",
        department="IT"
    )
    mock_repo.create.return_value = created_user
    
    use_case = CreateUserUseCase(mock_repo, mock_rabbitmq)
    request = CreateUserRequest(
        email="admin@example.com",
        full_name="Admin User",
        role="admin",
        phone="+1234567890",
        department="IT"
    )
    
    # Act
    result = await use_case.execute(request)
    
    # Assert
    assert result.phone == "+1234567890"
    assert result.department == "IT"
    assert result.role == "admin"


@pytest.mark.asyncio
async def test_create_user_publishes_event(mock_rabbitmq):
    """Test that user creation publishes RabbitMQ event."""
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.find_by_email.return_value = None
    
    created_user = User(
        id="event-test",
        email="event@example.com",
        full_name="Event User",
        role="user"
    )
    mock_repo.create.return_value = created_user
    
    use_case = CreateUserUseCase(mock_repo, mock_rabbitmq)
    request = CreateUserRequest(
        email="event@example.com",
        full_name="Event User"
    )
    
    # Act
    await use_case.execute(request)
    
    # Assert
    mock_rabbitmq.publish.assert_called_once()
    call_args = mock_rabbitmq.publish.call_args
    assert call_args[0][0] == "user.events"
    
    event = call_args[0][1]
    assert event["event_type"] == "user.created"
    assert event["user_id"] == "event-test"
    assert event["email"] == "event@example.com"