import contextlib
from sqlalchemy import delete
from fastapi_async_sqlalchemy import db

from src.schemas.user import UserCreate
from src.modules.auth.manager import get_user_manager
from src.models.user import get_user_db
from src.db.session import get_async_session
from src.models import User, Location, BookLocation


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False, is_verified: bool = True):
    async with get_async_session_context() as session:
        async with get_user_db_context(session) as user_db:
            async with get_user_manager_context(user_db) as user_manager:
                user = await user_manager.create(
                    UserCreate(
                        email=email, password=password, is_superuser=is_superuser, is_verified=is_verified
                    )
                )


async def create_dummy_data():
    dummy_location_1 = Location(
        name="Dummy Location 1",
        address="Dummy Address 1",
    )
    dummy_location_2 = Location(
        name="Dummy Location 2",
        address="Dummy Address 2",
    )

    async with db():
        # Clear up database
        await db.session.execute(delete(User))
        await db.session.execute(delete(BookLocation))
        await db.session.execute(delete(Location))

        # Create dummy data
        db.session.add_all([dummy_location_1, dummy_location_2])

        await db.session.commit()

    # Create dummy users
    await create_user(
        "admin@gmail.com",
        "admin",
        True,
        True
    )
    await create_user(
        "test@gmail.com",
        "test",
        False,
        True
    )
