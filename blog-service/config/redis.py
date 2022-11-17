import redis
from django.conf import settings

redis_client = None


def get_redis_client():
    global redis_client
    if not redis_client:
        redis_client = redis.from_url(settings.REDIS_URL)

    return redis_client
