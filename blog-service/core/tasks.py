import logging
from dataclasses import asdict, dataclass
from django.apps import apps as django_apps
from typing import Literal
from django.conf import settings
from django.db import IntegrityError
from redis import RedisError, Redis
from celery import shared_task
from celery.signals import celeryd_init
from config.redis import get_redis_client
from core.models import Article, Comment
from users.models import BlogUser

logger = logging.getLogger(__name__)


@dataclass
class LikeEvent:
    user_id: str
    obj_id: str
    obj_type: Literal['article', 'comment']
    creator_id: str


@shared_task
def send_like_event(user_id: str, obj_id: str, content_type_str: str):
    """
    Args:
        user_id (str): User who liked the object
        obj_id (str): The id of the object
        obj_type (object): The type of the object
    """
    obj_type = django_apps.get_model(content_type_str)
    if not hasattr(obj_type, 'creator'):
        raise ValueError("Unsupported Django model for sending like events.")
    redis_client = get_redis_client()
    stream = settings.REDIS_LIKES_STREAM

    try:
        obj = obj_type.objects.select_related('creator').get(pk=obj_id)
        user = BlogUser.objects.get(pk=user_id)
        like_event = LikeEvent(
            user_id=user.pk,
            obj_id=obj.pk,
            obj_type=obj_type.__name__.lower(),
            creator_id=obj.creator.pk
        )

        redis_client.xadd(
            name=stream,
            fields=asdict(like_event),
            id='*',
            maxlen=200
        )
    except BlogUser.DoesNotExist:
        logger.error(f"User: {user_id} doesn't exist anymore.")
    except obj_type.DoesNotExist:
        logger.error(f"Object ({obj_type.__name__}): {obj_id} doesn't exist or has been deleted at the time of the event.")
    except RedisError as e:
        logger.error(f'Redis error: {e}')



@shared_task
def send_follow_event(user_id: str, obj_id: str, obj_type: object):
    """
    Args:
        user_id (str): User who followed the object
        obj_id (str): The id of the object
        obj_type (object): The type of the object
    """
    pass


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
            if response:
                # We get a list of lists each containing name and one tuple of
                # entry id and data in a stream.
                last_id, data = response[0][1][0]
                BlogUser.objects.create_from_event(data)
        except RedisError as e:
            logger.error(f'Redis error: {e}')
        except IntegrityError as e:
            logger.error(f'User may already exist. More details: {e}')


@celeryd_init.connect
def start_users_consumer(**kwargs):
    consume_new_users_stream.delay()
