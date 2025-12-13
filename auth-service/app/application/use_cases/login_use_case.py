from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

from app.domain.entities.user import User
from app.domain.entities.token import Token, TokenPayload
from app.domain.repositories.user_repository import IUserRepository
from app.application.dtos.auth_dto import LoginRequest, LoginResponse
from app.infrastructure.cache.redis_client import RedisClient
from app.infrastructure.messaging.rabbitmq_publisher import RabbitMQPublisher


class LoginUseCase:
    """Use case for user authentication."""
    
    def __init__(
        self,
        user_repository: IUserRepository,
        redis_client: RedisClient,
        rabbitmq_publisher: RabbitMQPublisher,
        jwt_secret: str,
        jwt_algorithm: str,
        access_token_expire_minutes: int,
        refresh_token_expire_days: int
    ):
        self.user_repository = user_repository
        self.redis_client = redis_client
        self.rabbitmq_publisher = rabbitmq_publisher
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    async def execute(self, request: LoginRequest) -> LoginResponse:
        """
        Execute login use case.
        
        Args:
            request: Login credentials
            
        Returns:
            LoginResponse with tokens and user data
            
        Raises:
            ValueError: If credentials are invalid
        """
        # Find user by email
        user = await self.user_repository.find_by_email(request.email)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not self.pwd_context.verify(request.password, user.hashed_password):
            raise ValueError("Invalid email or password")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is deactivated")
        
        # Generate tokens
        access_token = self._create_access_token(user)
        refresh_token = self._create_refresh_token(user)
        
        # Store refresh token in Redis
        await self._store_refresh_token(user.id, refresh_token)
        
        # Publish login event
        await self._publish_login_event(user)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
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
    
    def _create_access_token(self, user: User) -> str:
        """Create JWT access token."""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def _create_refresh_token(self, user: User) -> str:
        """Create JWT refresh token."""
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "user_id": user.id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    async def _store_refresh_token(self, user_id: str, token: str) -> None:
        """Store refresh token in Redis with expiration."""
        key = f"refresh_token:{user_id}"
        ttl = self.refresh_token_expire_days * 24 * 60 * 60  # seconds
        await self.redis_client.set(key, token, ttl)
    
    async def _publish_login_event(self, user: User) -> None:
        """Publish user login event to RabbitMQ."""
        event = {
            "event_type": "user.logged_in",
            "user_id": user.id,
            "email": user.email,
            "timestamp": datetime.utcnow().isoformat(),
            "ip_address": None  # Will be added by controller
        }
        await self.rabbitmq_publisher.publish("auth.events", event)