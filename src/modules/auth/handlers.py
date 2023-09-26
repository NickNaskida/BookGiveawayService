import logging
from enum import Enum

logger = logging.getLogger(__name__)


class AuthEvent(Enum):
    REGISTERED = "registered"
    FORGOT_PASSWORD = "forgot_password"
    REQUESTED_VERIFY = "requested_verify"
    USER_UPDATED = "user_updated"


async def handle_register(user) -> None:
    """
    User registration event handler function.

    :param user: User that registered.
    :return: None
    """
    logger.info(f"User {user.id} has registered.")


async def handle_forgot_password(user, token) -> None:
    """
    Forgot password event handler function.

    :param user: User that requested the password reset.
    :param token: Generated token for the password reset.
    :return: None
    """
    logger.info(f"User {user.id} has forgot their password. Reset token: {token}")
    print(f"User {user.id} has forgot their password. Reset token: {token}")
    logger.info(f"Send reset email to {user.id}.")


async def handle_request_verify(user, token) -> None:
    """
    Email verification event handler function.

    :param user: User that requested the email verification.
    :param token: Generated token for the email verification.
    :return: None
    """
    logger.info(f"Verification requested for user {user.id}. Verification token: {token}")
    print(f"Verification requested for user {user.id}. Verification token: {token}")
    logger.info(f"Send verification email to {user.id}.")


event_handlers = {
    AuthEvent.REGISTERED: handle_register,
    AuthEvent.FORGOT_PASSWORD: handle_forgot_password,
    AuthEvent.REQUESTED_VERIFY: handle_request_verify,
    AuthEvent.USER_UPDATED: handle_request_verify,
}
