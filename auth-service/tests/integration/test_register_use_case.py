import pytest
from unittest.mock import AsyncMock
from app.domain.entities.user import User
from app.application.use_cases.register_use_case import RegisterUseCase
from app.application.dtos.auth_dto import RegisterRequest


@pytest.fixture
def register_use_case():
    return RegisterUseCase(
        user_repository=AsyncMock(),
        rabbitmq_publisher=AsyncMock()
    )


@pytest.mark.asyncio
async def test_register_success(register_use_case):
    # Mock find_by_email returns None (email not exists)
    register_use_case.user_repository.find_by_email.return_value = None
    
    # Mock create returns actual User entity
    created_user = User(
        id="new-user-id",
        email="new@example.com",
        hashed_password="hashed",
        full_name="New User"
    )
    register_use_case.user_repository.create.return_value = created_user
    
    request = RegisterRequest(
        email="new@example.com",
        password="Test123456",
        full_name="New User"
    )
    
    response = await register_use_case.execute(request)
    
    assert response.email == "new@example.com"
    assert response.full_name == "New User"
    assert register_use_case.user_repository.create.called


@pytest.mark.asyncio
async def test_register_email_exists(register_use_case):
    existing_user = User(
        email="existing@example.com",
        hashed_password="hash",
        full_name="Existing"
    )
    register_use_case.user_repository.find_by_email.return_value = existing_user
    
    request = RegisterRequest(
        email="existing@example.com",
        password="Test123456",
        full_name="New User"
    )
    
    with pytest.raises(ValueError, match="Email already registered"):
        await register_use_case.execute(request)