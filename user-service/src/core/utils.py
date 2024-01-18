import hashlib

import core.models
import redis.asyncio as aioredis
from config import get_settings


def hash_password(password: str):
    """Returns a salted password hash."""
    settings = get_settings()
    return hashlib.sha512(
        password.encode() + settings.password_salt.encode()
    ).hexdigest()


async def get_user_from_reset_token(token: str, redis: aioredis.Redis):
    user_id = await redis.get(f"pw-reset:{token}")
    reason = None
    user = None

    if not user_id:
        reason = "Token is invalid or has expired"
    else:
        user = await core.models.User.get(user_id)
        if not user:
            reason = "User does not exist anymore."

    return user, reason
