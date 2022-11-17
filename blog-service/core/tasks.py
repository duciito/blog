from django.conf import settings
from redis import RedisError, Redis
from celery import shared_task
from config.redis import get_redis_client


@shared_task
def consume_new_users_stream():
    redis_client: Redis = get_redis_client()
    stream = settings.REDIS_NEW_USERS_STREAM

    while True:
        try:
            user = redis_client.xread(

            )
        except RedisError:
            pass
