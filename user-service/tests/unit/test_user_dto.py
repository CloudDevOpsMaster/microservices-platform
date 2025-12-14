import pytest
from pydantic import ValidationError
from app.application.dtos.user_dto import CreateUserRequest, UpdateUserRequest


def test_create_user_request_valid():
    """Test valid CreateUserRequest."""
    request = CreateUserRequest(
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    
    assert request.email == "test@example.com"
    assert request.full_name == "Test User"
    assert request.role == "user"


def test_create_user_request_with_optional():
    """Test CreateUserRequest with optional fields."""
    request = CreateUserRequest(
        email="test@example.com",
        full_name="Test User",
        phone="+1234567890",
        department="Engineering"
    )
    
    assert request.phone == "+1234567890"
    assert request.department == "Engineering"


def test_create_user_request_invalid_email():
    """Test CreateUserRequest with invalid email."""
    with pytest.raises(ValidationError):
        CreateUserRequest(
            email="invalid-email",
            full_name="Test User"
        )


def test_create_user_request_short_name():
    """Test CreateUserRequest with short name."""
    with pytest.raises(ValidationError):
        CreateUserRequest(
            email="test@example.com",
            full_name="A"
        )


def test_create_user_request_invalid_role():
    """Test CreateUserRequest with invalid role."""
    with pytest.raises(ValidationError):
        CreateUserRequest(
            email="test@example.com",
            full_name="Test User",
            role="superuser"
        )


def test_create_user_request_strips_whitespace():
    """Test that full_name whitespace is stripped."""
    request = CreateUserRequest(
        email="test@example.com",
        full_name="  Test User  "
    )
    
    assert request.full_name == "Test User"


def test_update_user_request_valid():
    """Test valid UpdateUserRequest."""
    request = UpdateUserRequest(
        full_name="Updated Name",
        phone="+9876543210"
    )
    
    assert request.full_name == "Updated Name"
    assert request.phone == "+9876543210"


def test_update_user_request_all_none():
    """Test UpdateUserRequest with all None values."""
    request = UpdateUserRequest()
    
    assert request.full_name is None
    assert request.phone is None
    assert request.department is None