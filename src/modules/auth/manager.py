import uuid
from typing import Optional, Union, Dict, Any

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, InvalidPasswordException
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy, BearerTransport
from fastapi_users.db import SQLAlchemyUserDatabase


from src.core.config import settings
from src.models.user import User, get_user_db
from src.schemas.user import UserCreate
from src.modules.auth.handlers import event_handlers, AuthEvent


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.SECRET
    verification_token_secret = settings.SECRET

    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ) -> None:
        await event_handlers[AuthEvent.REGISTERED](user)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        await event_handlers[AuthEvent.FORGOT_PASSWORD](user, token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        await event_handlers[AuthEvent.REQUESTED_VERIFY](user, token)

    async def on_after_update(
        self, user: User, update_dict: Dict[str, Any], request: Optional[Request] = None
    ) -> None:
        await event_handlers[AuthEvent.USER_UPDATED](user, update_dict)

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 4:
            raise InvalidPasswordException(
                reason="Password too short",
            )


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl=settings.API_V1_STR + "/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

auth_core = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
