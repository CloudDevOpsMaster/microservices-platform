import pytest
from unittest.mock import AsyncMock, MagicMock
from passlib.context import CryptContext

from app.domain.entities.user import User
from app.application.use_cases.login_use_case import LoginUseCase
from app.application.dtos.auth_dto import LoginRequest


@pytest.fixture
def mock_user_repository():
    """Mock user repository."""
    return AsyncMock()


@pytest.fixture
def mock_redis_client():
    """Mock Redis client."""
    return AsyncMock()


@pytest.fixture
def mock_rabbitmq_publisher():
    """Mock RabbitMQ publisher."""
    return AsyncMock()


@pytest.fixture
def login_use_case(mock_user_repository, mock_redis_client, mock_rabbitmq_publisher):
    """Create login use case instance."""
    return LoginUseCase(
        user_repository=mock_user_repository,
        redis_client=mock_redis_client,
        rabbitmq_publisher=mock_rabbitmq_publisher,
        jwt_secret="test_secret",
        jwt_algorithm="HS256",
        access_token_expire_minutes=30,
        refresh_token_expire_days=7
    )


@pytest.mark.asyncio
async def test_login_success(login_use_case, mock_user_repository):
    """Test successful login."""
    # Arrange
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("Test123456")
    
    user = User(
        id="user123",
        email="test@example.com",
        hashed_password=hashed_password,
        full_name="Test User",
        is_active=True
    )
    
    mock_user_repository.find_by_email.return_value = user
    request = LoginRequest(email="test@example.com", password="Test123456")
    
    # Act
    response = await login_use_case.execute(request)
    
    # Assert
    assert response.access_token is not None
    assert response.refresh_token is not None
    assert response.token_type == "bearer"
    assert response.user["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_login_invalid_email(login_use_case, mock_user_repository):
    """Test login with invalid email."""
    # Arrange
    mock_user_repository.find_by_email.return_value = None
    request = LoginRequest(email="nonexistent@example.com", password="Test123456")
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid email or password"):
        await login_use_case.execute(request)


@pytest.mark.asyncio
async def test_login_invalid_password(login_use_case, mock_user_repository):
    """Test login with invalid password."""
    # Arrange
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("CorrectPassword")
    
    user = User(
        email="test@example.com",
        hashed_password=hashed_password,
        full_name="Test User"
    )
    
    mock_user_repository.find_by_email.return_value = user
    request = LoginRequest(email="test@example.com", password="WrongPassword")
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid email or password"):
        await login_use_case.execute(request)


@pytest.mark.asyncio
async def test_login_inactive_user(login_use_case, mock_user_repository):
    """Test login with inactive user."""
    # Arrange
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash("Test123456")
    
    user = User(
        email="test@example.com",
        hashed_password=hashed_password,
        full_name="Test User",
        is_active=False
    )
    
    mock_user_repository.find_by_email.return_value = user
    request = LoginRequest(email="test@example.com", password="Test123456")
    
    # Act & Assert
    with pytest.raises(ValueError, match="User account is deactivated"):
        await login_use_case.execute(request)