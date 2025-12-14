from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class CreateUserRequest(BaseModel):
    """DTO for creating a user."""
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="user", pattern="^(user|admin|moderator)$")
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=50)
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Full name cannot be empty')
        return v.strip()


class UpdateUserRequest(BaseModel):
    """DTO for updating a user."""
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    department: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, pattern="^(user|admin|moderator)$")
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    """DTO for user response."""
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool
    is_verified: bool
    phone: Optional[str] = None
    department: Optional[str] = None
    created_at: str
    updated_at: str
    
    model_config = {
        "from_attributes": True
    }


class UserListResponse(BaseModel):
    """DTO for paginated user list."""
    users: list[UserResponse]
    total: int
    skip: int
    limit: int