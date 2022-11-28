import logging
from django.conf import settings
from redis import RedisError, Redis
from celery import shared_task
from celery.signals import celeryd_init
from config.redis import get_redis_client

logger = logging.getLogger(__name__)


@shared_task
def consume_new_users_stream():
    redis_client: Redis = get_redis_client()
    stream = settings.REDIS_NEW_USERS_STREAM
    last_id = None

    while True:
        try:
            # Start with getting the latest entry at the point of running
            # this task and block for 5s before getting a new entry.
            response = redis_client.xread(
                {stream: last_id if last_id else '$'},
                count=1,
                block=5000
            )
            logger.info(response)
        except RedisError as e:
            logger.error(str(e))


@celeryd_init.connect
def start_users_consumer(sender=None, conf=None, **kwargs):
    consume_new_users_stream.delay()
