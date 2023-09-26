import redis.asyncio

from src.core.config import settings
from src.core.utils import get_redis_uri

auth_redis = redis.asyncio.from_url(get_redis_uri(settings.REDIS_SESSION_DB), decode_responses=True)
