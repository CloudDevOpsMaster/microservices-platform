from datetime import datetime, timedelta
import jwt
from typing import Optional

from app.domain.repositories.user_repository import IUserRepository
from app.application.dtos.auth_dto import RefreshTokenRequest, LoginResponse
from app.infrastructure.cache.redis_client import RedisClient


class RefreshTokenUseCase:
    """Use case for refreshing access tokens."""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        redis_client: RedisClient,
        jwt_secret: str,
        jwt_algorithm: str,
        access_token_expire_minutes: int
    ):
        self.user_repository = user_repository
        self.redis_client = redis_client
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
    
    async def execute(self, request: RefreshTokenRequest) -> LoginResponse:
        """
        Execute refresh token use case.
        
        Args:
            request: Refresh token request
            
        Returns:
            LoginResponse with new access token
            
        Raises:
            ValueError: If refresh token is invalid
        """
        try:
            # Decode refresh token
            payload = jwt.decode(
                request.refresh_token,
                self.jwt_secret,
                algorithms=[self.jwt_algorithm]
            )
            
            # Validate token type
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")
            
            user_id = payload.get("user_id")
            if not user_id:
                raise ValueError("Invalid token payload")
            
            # Verify token exists in Redis
            stored_token = await self.redis_client.get(f"refresh_token:{user_id}")
            if stored_token != request.refresh_token:
                raise ValueError("Token has been revoked")
            
            # Get user
            user = await self.user_repository.find_by_id(user_id)
            if not user or not user.is_active:
                raise ValueError("User not found or inactive")
            
            # Generate new access token
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            new_payload = {
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "access"
            }
            access_token = jwt.encode(new_payload, self.jwt_secret, algorithm=self.jwt_algorithm)
            
            return LoginResponse(
                access_token=access_token,
                refresh_token=request.refresh_token,
                token_type="bearer",
                expires_in=self.access_token_expire_minutes * 60,
                user={
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role,
                    "is_verified": user.is_verified
                }
            )
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid refresh token")