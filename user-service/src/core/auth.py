import base64
from datetime import timedelta

from config import get_settings
from core.models import User
from core.schemas import TokensSchema
from fastapi import WebSocket
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import RevokedTokenError
from pydantic import BaseModel
from redis_conf import get_redis_client

DENYLIST_PREFIX = "token-denylist"
settings = get_settings()


class AuthSettings(BaseModel):
    authjwt_algorithm: str = settings.jwt_algorithm
    authjwt_public_key: str = base64.b64decode(settings.jwt_public_key).decode("utf-8")
    authjwt_private_key: str = base64.b64decode(settings.jwt_private_key).decode(
        "utf-8"
    )


@AuthJWT.load_config
def get_config():
    return AuthSettings()


async def jwt_required_async(
    self,
    auth_from: str = "request",
    token: str | None = None,
    websocket: WebSocket | None = None,
    csrf_token: str | None = None,
) -> None:
    """Addition to AuthJWT so we can use redis asynchronously."""
    self.jwt_required(auth_from, token, websocket, csrf_token)
    token_id = self.get_raw_jwt()["jti"]
    redis = get_redis_client()

    if await redis.exists(f"{DENYLIST_PREFIX}:{token_id}"):
        raise RevokedTokenError(status_code=401, message="Token has been revoked")


def create_access_token(user: User, auth: AuthJWT) -> str:
    return auth.create_access_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=settings.access_token_expiration),
        headers={"kid": settings.jwt_sig_kid},
    )


def create_tokens(user: User, auth: AuthJWT) -> TokensSchema:
    access_token = create_access_token(user, auth)
    refresh_token = auth.create_refresh_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=settings.refresh_token_expiration),
    )
    return TokensSchema(access_token=access_token, refresh_token=refresh_token)
