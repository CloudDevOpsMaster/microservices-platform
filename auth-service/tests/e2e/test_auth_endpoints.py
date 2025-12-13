import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/auth/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_register_endpoint_validation():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Invalid email
        response = await client.post("/auth/register", json={
            "email": "invalid",
            "password": "Test123456",
            "full_name": "Test"
        })
        assert response.status_code == 422
        
        # Weak password
        response = await client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "weak",
            "full_name": "Test"
        })
        assert response.status_code == 422