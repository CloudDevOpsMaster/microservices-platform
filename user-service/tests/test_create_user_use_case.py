import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.entities.user import User
from app.application.use_cases.create_user_use_case import CreateUserUseCase
from app.application.dtos.user_dto import CreateUserRequest


@pytest.mark.asyncio
async def test_create_user_success():
    """Test successful user creation."""
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.find_by_email.return_value = None
    mock_repo.create.return_value = User(
        id="123",
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    
    mock_rabbitmq = AsyncMock()
    
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
    mock_repo.create.assert_called_once()
    mock_rabbitmq.publish.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_email_exists():
    """Test user creation with existing email."""
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.find_by_email.return_value = User(
        id="existing",
        email="test@example.com",
        full_name="Existing User",
        role="user"
    )
    
    mock_rabbitmq = AsyncMock()
    
    use_case = CreateUserUseCase(mock_repo, mock_rabbitmq)
    request = CreateUserRequest(
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    
    # Act & Assert
    with pytest.raises(ValueError, match="Email already registered"):
        await use_case.execute(request)