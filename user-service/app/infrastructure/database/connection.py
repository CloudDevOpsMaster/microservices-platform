# user-service/app/infrastructure/database/connection.py
"""
Database connection management for User Service.
Handles PostgreSQL connections with async support and proper lifecycle.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData
import logging

logger = logging.getLogger(__name__)

# SQLAlchemy Base with naming convention for constraints
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
Base = declarative_base(metadata=metadata)


class DatabaseConnection:
    """
    Manages database connections for User Service.
    Provides async engine and session management.
    """
    
    def __init__(self, database_url: str):
        """
        Initialize database connection manager.
        
        Args:
            database_url: PostgreSQL connection URL
        """
        self.database_url = database_url
        self.engine = None
        self.async_session_maker = None
        
    async def connect(self) -> None:
        """
        Establish database connection and create engine.
        """
        try:
            self.engine = create_async_engine(
                self.database_url,
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
            
            self.async_session_maker = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
            
            logger.info("Database connection established")
            
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    async def disconnect(self) -> None:
        """
        Close database connections gracefully.
        """
        if self.engine:
            try:
                await self.engine.dispose()
                logger.info("Database connections closed")
            except Exception as e:
                logger.error(f"Error disconnecting from database: {e}")
    
    async def create_tables(self) -> None:
        """
        Create all tables defined in Base metadata.
        """
        if not self.engine:
            raise RuntimeError("Database engine not initialized")
        
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            raise
    
    async def drop_tables(self) -> None:
        """
        Drop all tables (use with caution, mainly for testing).
        """
        if not self.engine:
            raise RuntimeError("Database engine not initialized")
        
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.info("Database tables dropped")
        except Exception as e:
            logger.error(f"Error dropping tables: {e}")
            raise
    
    def get_session(self) -> AsyncSession:
        """
        Get a new database session.
        
        Returns:
            AsyncSession: Database session
            
        Example:
            async with db_connection.get_session() as session:
                result = await session.execute(select(User))
                users = result.scalars().all()
        """
        if not self.async_session_maker:
            raise RuntimeError("Session maker not initialized")
        
        return self.async_session_maker()
    
    async def health_check(self) -> bool:
        """
        Check if database connection is healthy.
        
        Returns:
            bool: True if healthy, False otherwise
        """
        if not self.engine:
            return False
        
        try:
            async with self.engine.connect() as conn:
                await conn.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    @property
    def is_connected(self) -> bool:
        """
        Check if database is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        return self.engine is not None and self.async_session_maker is not None