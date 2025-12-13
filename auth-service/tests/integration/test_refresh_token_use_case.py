import pytest
from unittest.mock import AsyncMock
import jwt
from datetime import datetime, timedelta
from app.domain.entities.user import User
from app.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.application.dtos.auth_dto import RefreshTokenRequest


@pytest.fixture
def refresh_use_case():
    return RefreshTokenUseCase(
        user_repository=AsyncMock(),
        redis_client=AsyncMock(),
        jwt_secret="test_secret",
        jwt_algorithm="HS256",
        access_token_expire_minutes=30
    )


@pytest.mark.asyncio
async def test_refresh_token_success(refresh_use_case):
    user = User(
        id="user123",
        email="test@example.com",
        hashed_password="hash",
        full_name="Test User"
    )
    
    # Create valid refresh token
    payload = {
        "user_id": "user123",
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, "test_secret", algorithm="HS256")
    
    refresh_use_case.redis_client.get.return_value = token
    refresh_use_case.user_repository.find_by_id.return_value = user
    
    request = RefreshTokenRequest(refresh_token=token)
    response = await refresh_use_case.execute(request)
    
    assert response.access_token is not None
    assert response.user["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_refresh_token_expired(refresh_use_case):
    payload = {
        "user_id": "user123",
        "type": "refresh",
        "exp": datetime.utcnow() - timedelta(days=1)  # Expired
    }
    token = jwt.encode(payload, "test_secret", algorithm="HS256")
    
    request = RefreshTokenRequest(refresh_token=token)
    
    with pytest.raises(ValueError, match="expired"):
        await refresh_use_case.execute(request)