from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class Token:
    """Domain entity representing an authentication token."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutes in seconds
    
    @property
    def expires_at(self) -> datetime:
        """Calculate token expiration time."""
        return datetime.utcnow() + timedelta(seconds=self.expires_in)


@dataclass
class TokenPayload:
    """Token payload data."""
    
    user_id: str
    email: str
    role: str
    exp: datetime
    iat: datetime = None
    
    def __post_init__(self):
        if self.iat is None:
            self.iat = datetime.utcnow()