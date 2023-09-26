from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.db.utils import engine_args
from src.core.utils import get_sqlalchemy_uri

SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri()

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URI,
    **engine_args
)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
