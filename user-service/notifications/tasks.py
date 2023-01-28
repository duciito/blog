import logging
import redis.asyncio as aioredis

from config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


async def consume_like_events(redis: aioredis.Redis):
    stream = settings.redis_likes_stream
    last_id = None

    while True:
        try:
            resp = await redis.xread(
                {stream: last_id or '$'},
                count = 1,
                block=5000
            )
            print(resp)
            if resp:
                # We get a list of lists each containing name and one tuple of
                # entry id and data in a stream.
                last_id, data = resp[0][1][0]
                logger.debug(data)
        except aioredis.RedisError as e:
            logger.error(f'Redis error: {e}')
