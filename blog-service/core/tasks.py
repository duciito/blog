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
            # [[b'new-users', [(b'1669744006942-0', {b'id': b'63864586e5db203fa4ba5840', b'email': b'daniel.ivanov+17@mentormate.com', b'first_name': b'string', b'last_name': b'string', b'profile_description': b'string', b'joined_at': b'2022-11-04T17:19:27.744000+00:00'})]]]
        except RedisError as e:
            logger.error(f'Redis error: {str(e)}')


@celeryd_init.connect
def start_users_consumer(sender=None, conf=None, **kwargs):
    consume_new_users_stream.delay()
