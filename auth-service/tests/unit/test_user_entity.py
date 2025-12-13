import pytest
from datetime import datetime
from app.domain.entities.user import User


def test_user_creation_valid():
    """Test valid user creation."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_pwd",
        full_name="Test User"
    )
    
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.is_verified is False
    assert user.role == "user"


def test_user_creation_invalid_email():
    """Test user creation with invalid email."""
    with pytest.raises(ValueError, match="Invalid email format"):
        User(
            email="invalid-email",
            hashed_password="hashed_pwd",
            full_name="Test User"
        )


def test_user_creation_invalid_name():
    """Test user creation with invalid name."""
    with pytest.raises(ValueError, match="Full name must be at least 2 characters"):
        User(
            email="test@example.com",
            hashed_password="hashed_pwd",
            full_name="A"
        )


def test_user_deactivate():
    """Test user deactivation."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_pwd",
        full_name="Test User"
    )
    
    user.deactivate()
    assert user.is_active is False


def test_user_verify_email():
    """Test email verification."""
    user = User(
        email="test@example.com",
        hashed_password="hashed_pwd",
        full_name="Test User"
    )
    
    user.verify_email()
    assert user.is_verified is True