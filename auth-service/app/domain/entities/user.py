from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class User:
    """Domain entity representing a user."""
    
    # Campos sin default primero
    email: str
    hashed_password: str
    full_name: str
    
    # Campos con default después
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_active: bool = True
    is_verified: bool = False
    role: str = "user"
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate domain rules."""
        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email format")
        if not self.full_name or len(self.full_name.strip()) < 2:
            raise ValueError("Full name must be at least 2 characters")
        if self.role not in ["user", "admin", "moderator"]:
            raise ValueError("Invalid role")
    
    def deactivate(self) -> None:
        """Deactivate user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def verify_email(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.updated_at = datetime.utcnow()