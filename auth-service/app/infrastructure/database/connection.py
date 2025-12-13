from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from app.infrastructure.database.models import Base

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Database connection manager."""
    
    def __init__(self, database_url: str):
        # Convert sync URL to async
        self.database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        self.engine = None
        self.session_factory = None
    
    async def connect(self) -> None:
        """Initialize database connection."""
        try:
            self.engine = create_async_engine(
                self.database_url,
                echo=False,
                poolclass=NullPool,
                future=True
            )
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")
    
    async def create_tables(self) -> None:
        """Create all database tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created")
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise