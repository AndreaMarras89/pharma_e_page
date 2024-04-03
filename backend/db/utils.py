"""Database connection and utilities"""

import asyncio
import contextlib

from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base


from backend.configuration import config

Base = declarative_base()


class DatabaseSessionMaker:
    """Asynchronous database session."""

    def __init__(self) -> None:
        self.database_url = config.database_url
        self.engine = create_async_engine(
            self.database_url,
            isolation_level="AUTOCOMMIT",
            
        )
        self.async_session = async_sessionmaker(
            bind=self.engine,
        )

    async def init_db(self):
        """Initialize database."""
        
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """Getter for database session."""
        
        session = self.async_session()
        try:
            yield session
        except SQLAlchemyError:
            raise
        finally:
            await asyncio.shield(session.close())
        