from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional

security = HTTPBearer()


class AuthMiddleware:
    """JWT authentication middleware."""
    
    def __init__(self, jwt_secret: str, jwt_algorithm: str):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
    
    async def verify_token(self, credentials: HTTPAuthorizationCredentials) -> dict:
        """
        Verify JWT token and extract payload.
        
        Args:
            credentials: HTTP authorization credentials
            
        Returns:
            Token payload
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            token = credentials.credentials
            payload = jwt.decode(
                token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
            
            # Verify token type
            if payload.get("type") != "access":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    async def get_current_user(self, credentials: HTTPAuthorizationCredentials) -> dict:
        """Get current authenticated user from token."""
        payload = await self.verify_token(credentials)
        return {
            "user_id": payload.get("user_id"),
            "email": payload.get("email"),
            "role": payload.get("role")
        }