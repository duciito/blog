import json

import redis.asyncio as aioredis
from config import get_settings
from core.models import User

settings = get_settings()


async def add_user_to_stream(user: User, redis: aioredis.Redis):
    # `revision_id` comes from Mongo's default model.
    return await redis.xadd(
        name=settings.redis_new_users_stream,
        fields=json.loads(user.json(exclude={"revision_id", "password"})),
        id="*",
        maxlen=50,
    )
