import os
from pathlib import Path
from typing import List, Union

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class DevSettings(BaseSettings):
    """
    Settings for development environment.
    """
    DEBUG: bool = True
    SECRET: str = "NOT_A_SECRET"

    # API
    API_HOST: str = "localhost"
    API_PORT: int = 8000
    API_V1_STR: str = "/api/v1"

    # Logging
    LOG_LEVEL: str = "DEBUG"

    # Project
    PROJECT_NAME: str = "Book Giveaway Service"
    PROJECT_VERSION: str = "0.1.0"

    DOC_URL: Union[str, None] = "/"
    REDOC_URL: Union[str, None] = "/redoc"

    # CORS
    BACKEND_CORS_ORIGINS: List = ["http://localhost:3000"]

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int

    # Environment
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, "envs/.env"),
        env_file_encoding='utf-8'
    )


class TestSettings(DevSettings):
    """
    Settings for test environment.
    """
    DEBUG: bool = True
    TESTING: bool = True


class ProdSettings(DevSettings):
    """
    Settings for production environment.
    """
    DEBUG: bool = False

    LOG_LEVEL: str = "INFO"

    # Project
    DOC_URL: Union[str, None] = None
    REDOC_URL: Union[str, None] = None


settings = DevSettings()
