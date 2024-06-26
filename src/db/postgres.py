from typing import Generator
import logging

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from src.core.config import DATABASE_URL, SHOW_SQL_QUERY

engine = create_async_engine(DATABASE_URL, echo=SHOW_SQL_QUERY)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

logger = logging.getLogger(__name__)


async def get_db_session() -> Generator:
    """Dependency for getting async session"""
    async with async_session_maker() as session:
        yield session
