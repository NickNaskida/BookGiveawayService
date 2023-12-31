from fastapi import APIRouter

from src.modules.auth.manager import auth_core, auth_backend
from src.schemas.user import UserRead, UserCreate
from src.modules.auth.routers import users_router
from src.api.api_v1.endpoints import (
    genre,
    author,
    book,
    pickup,
    request
)


api_router = APIRouter()

# Auth routes
api_router.include_router(
    auth_core.get_auth_router(auth_backend, requires_verification=True),
    prefix="/auth/jwt",
    tags=["auth"]
)
api_router.include_router(
    auth_core.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    auth_core.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    auth_core.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

# User routes
api_router.include_router(
    users_router,
    prefix="/users",
    tags=["user"],
)

# Genre routes
api_router.include_router(
    genre.router,
    prefix="/genres",
    tags=["genre"],
)

# Author routes
api_router.include_router(
    author.router,
    prefix="/authors",
    tags=["author"],
)

# Book routes
api_router.include_router(
    book.router,
    prefix="/books",
    tags=["book"],
)

# Pickup routes
api_router.include_router(
    pickup.router,
    prefix="/pickup-locations",
    tags=["pickup-location"],
)

# Request routes
api_router.include_router(
    request.router,
    prefix="/book-requests",
    tags=["book-request"],
)
