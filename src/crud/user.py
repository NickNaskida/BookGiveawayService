from typing import Optional, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.crud.base import CRUDBase
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get(self, _id: Any, db_session: AsyncSession | None = None) -> Optional[User]:
        db_session = db_session or self.db.session
        query = select(self.model).where(self.model.id == _id)
        response = await db_session.execute(query)
        return response.unique().scalar_one_or_none()

    async def get_by_email(self, email: str, db_session: AsyncSession | None = None) -> Optional[User]:
        db_session = db_session or self.get_db()
        query = await db_session.execute(select(User).where(User.email == email))
        return query.unique().scalar_one_or_none()


user = CRUDUser(User)
