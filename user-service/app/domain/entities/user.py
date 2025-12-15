from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
import uuid


@dataclass
class User:
    """Domain entity representing a user."""
    
    email: str
    full_name: str
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_active: bool = True
    is_verified: bool = False
    role: str = "user"
    phone: Optional[str] = None
    department: Optional[str] = None
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
    
    def update_profile(self, full_name: Optional[str] = None, 
                      phone: Optional[str] = None,
                      department: Optional[str] = None) -> None:
        """Update user profile."""
        if full_name:
            if len(full_name.strip()) < 2:
                raise ValueError("Full name must be at least 2 characters")
            self.full_name = full_name
        if phone:
            self.phone = phone
        if department:
            self.department = department
        self.updated_at = datetime.utcnow()
    
    def deactivate(self) -> None:
        """Deactivate user account."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate user account."""
        self.is_active = True
        self.updated_at = datetime.utcnow()