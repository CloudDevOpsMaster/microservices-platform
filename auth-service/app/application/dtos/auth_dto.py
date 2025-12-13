from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class LoginRequest(BaseModel):
    """Login request DTO."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)


class LoginResponse(BaseModel):
    """Login response DTO."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class RefreshTokenRequest(BaseModel):
    """Refresh token request DTO."""
    refresh_token: str


class RegisterRequest(BaseModel):
    """User registration request DTO."""
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=2, max_length=100)
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserResponse(BaseModel):
    """User response DTO."""
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    created_at: str