import pytest
from app.domain.entities.user import User


def test_user_creation_valid():
    """Test valid user creation."""
    user = User(
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.is_verified is False


def test_user_invalid_email():
    """Test user creation with invalid email."""
    with pytest.raises(ValueError, match="Invalid email format"):
        User(email="invalid", full_name="Test User")


def test_user_invalid_name():
    """Test user creation with invalid name."""
    with pytest.raises(ValueError, match="Full name must be at least 2 characters"):
        User(email="test@example.com", full_name="A")


def test_user_invalid_role():
    """Test user creation with invalid role."""
    with pytest.raises(ValueError, match="Invalid role"):
        User(email="test@example.com", full_name="Test User", role="invalid")


def test_user_update_profile():
    """Test user profile update."""
    user = User(email="test@example.com", full_name="Test User")
    user.update_profile(full_name="Updated Name", phone="123456")
    
    assert user.full_name == "Updated Name"
    assert user.phone == "123456"