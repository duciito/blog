import logging

import aioboto3
from config import get_settings

logger = logging.getLogger(__name__)


async def ses_verify_email_address(email):
    """Verify email so the user can receive subsequent emails."""
    settings = get_settings()
    session = aioboto3.Session(
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key,
        aws_secret_access_key=settings.aws_secret_key,
    )

    async with session.client("ses") as ses:
        try:
            await ses.verify_email_identity(EmailAddress=email)
        except Exception as e:
            logger.error(f"Unable to verify email '{email}': {e}")
