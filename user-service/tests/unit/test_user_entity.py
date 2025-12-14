import pytest
from datetime import datetime
from app.domain.entities.user import User


def test_user_creation_valid():
    """Test valid user creation."""
    user = User(
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.role == "user"
    assert user.is_active is True
    assert user.is_verified is False
    assert user.id is not None
    assert isinstance(user.created_at, datetime)


def test_user_creation_with_optional_fields():
    """Test user creation with optional fields."""
    user = User(
        email="test@example.com",
        full_name="Test User",
        role="admin",
        phone="+1234567890",
        department="Engineering"
    )
    
    assert user.phone == "+1234567890"
    assert user.department == "Engineering"
    assert user.role == "admin"


def test_user_invalid_email():
    """Test user creation with invalid email."""
    with pytest.raises(ValueError, match="Invalid email format"):
        User(email="invalid-email", full_name="Test User")


def test_user_invalid_empty_email():
    """Test user creation with empty email."""
    with pytest.raises(ValueError, match="Invalid email format"):
        User(email="", full_name="Test User")


def test_user_invalid_short_name():
    """Test user creation with short name."""
    with pytest.raises(ValueError, match="Full name must be at least 2 characters"):
        User(email="test@example.com", full_name="A")


def test_user_invalid_empty_name():
    """Test user creation with empty name."""
    with pytest.raises(ValueError, match="Full name must be at least 2 characters"):
        User(email="test@example.com", full_name="")


def test_user_invalid_role():
    """Test user creation with invalid role."""
    with pytest.raises(ValueError, match="Invalid role"):
        User(
            email="test@example.com",
            full_name="Test User",
            role="superuser"
        )


def test_user_update_profile():
    """Test user profile update."""
    user = User(email="test@example.com", full_name="Test User")
    original_updated_at = user.updated_at
    
    user.update_profile(
        full_name="Updated Name",
        phone="+9876543210",
        department="Sales"
    )
    
    assert user.full_name == "Updated Name"
    assert user.phone == "+9876543210"
    assert user.department == "Sales"
    assert user.updated_at > original_updated_at


def test_user_update_profile_invalid_name():
    """Test profile update with invalid name."""
    user = User(email="test@example.com", full_name="Test User")
    
    with pytest.raises(ValueError, match="Full name must be at least 2 characters"):
        user.update_profile(full_name="A")


def test_user_deactivate():
    """Test user deactivation."""
    user = User(email="test@example.com", full_name="Test User")
    assert user.is_active is True
    
    user.deactivate()
    
    assert user.is_active is False


def test_user_activate():
    """Test user activation."""
    user = User(
        email="test@example.com",
        full_name="Test User",
        is_active=False
    )
    assert user.is_active is False
    
    user.activate()
    
    assert user.is_active is True