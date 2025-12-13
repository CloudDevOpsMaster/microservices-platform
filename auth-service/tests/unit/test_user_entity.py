import pytest
from app.domain.entities.user import User

def test_user_creation_valid():
    user = User(email="test@example.com", hashed_password="hash", full_name="Test User")
    assert user.email == "test@example.com"
    assert user.is_active is True

def test_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email format"):
        User(email="invalid", hashed_password="hash", full_name="Test")

def test_user_deactivate():
    user = User(email="test@example.com", hashed_password="hash", full_name="Test")
    user.deactivate()
    assert user.is_active is False