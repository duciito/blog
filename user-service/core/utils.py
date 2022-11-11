import aioboto3
import logging
import hashlib
import redis.asyncio as aioredis

import core.models
from config import get_settings

logger = logging.getLogger(__name__)


def hash_password(password: str):
    """Returns a salted password hash."""
    settings = get_settings()
    return hashlib.sha512(
        password.encode() + settings.password_salt.encode()
    ).hexdigest()


async def ses_verify_email_address(email):
    """Verify email so the user can receive subsequent emails."""
    settings = get_settings()
    session = aioboto3.Session(
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key
    )

    async with session.client('ses') as ses:
        try:
            await ses.verify_email_identity(EmailAddress=email)
        except Exception as e:
            logger.error(f"Unable to verify email '{email}': {e}")


async def get_user_from_reset_token(token: str, redis: aioredis.Redis):
    user_id = await redis.get(f'pw-reset:{token}')
    reason = None
    user = None

    if not user_id:
        reason = 'Token is invalid or has expired'
    else:
        user = await core.models.User.get(user_id)
        if not user:
            reason = 'User does not exist anymore.'

    return user, reason
