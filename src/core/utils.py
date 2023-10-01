from src.core.config import settings


def get_sqlalchemy_uri() -> str:
    """
    Get the URI for the Postgres database.

    :return: The URI for the Postgres database.
    """
    host, port = settings.POSTGRES_HOST, settings.POSTGRES_PORT
    user, password = settings.POSTGRES_USER, settings.POSTGRES_PASSWORD
    db_name = settings.POSTGRES_DB
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url() -> str:
    """
    Get the URL for the API.

    :return: The URL for the API.
    """
    host, port = settings.API_HOST, settings.API_PORT
    api_url = settings.API_V1_STR
    debug = settings.DEBUG
    scheme = "https" if not debug else "http"

    return f"{scheme}://{host}:{port}" + api_url
