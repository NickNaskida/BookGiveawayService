from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from starlette_csrf import CSRFMiddleware

from src.db.utils import engine_args
from src.api.api_v1.api import api_router
from src.core.config import settings
from src.core.utils import get_sqlalchemy_uri
from src.core.logger import configure_logger


def create_app() -> FastAPI:
    configure_logger()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=settings.DOC_URL,
        redoc_url=settings.REDOC_URL,
    )

    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # app.add_middleware(
    #     CSRFMiddleware,
    #     secret=settings.SECRET,
    # )
    app.add_middleware(
        SQLAlchemyMiddleware,
        db_url=get_sqlalchemy_uri(),
        engine_args=engine_args
    )
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.SECRET
    )

    # Routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

