from datetime import datetime

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase
)
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.models.base import Base
from src.db.session import get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    """Base user model."""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
