from datetime import UTC, datetime, timedelta
from typing import Annotated
from uuid import uuid4

import jwt
from config import get_settings
from core.models import User
from core.schemas import AuthToken, TokensSchema
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services.redis import get_redis_client

DENYLIST_PREFIX = "token-denylist"

settings = get_settings()
bearer_scheme = HTTPBearer()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(user: User) -> str:
    exp = datetime.now(UTC) + timedelta(minutes=settings.access_token_expiration)
    data = {
        "sub": str(user.id),
        "jti": str(uuid4()),
        "exp": exp,
        "type": "access",
    }
    return jwt.encode(
        data,
        settings.jwt_private_key,
        algorithm="RS256",
        headers={"kid": settings.jwt_sig_kid},
    )


def create_tokens(user: User) -> TokensSchema:
    access_token = create_access_token(user)
    exp = datetime.now(UTC) + timedelta(minutes=settings.refresh_token_expiration)
    data = {
        "sub": str(user.id),
        "exp": exp,
        "type": "refresh",
    }
    refresh_token = jwt.encode(data, settings.jwt_private_key, algorithm="RS256")
    return TokensSchema(access_token=access_token, refresh_token=refresh_token)


class AuthDep:
    """Middleware for auth protected routes which verifies the JWT."""

    def __init__(self, token_type: str = "access"):
        self.token_type = token_type
        self.redis = get_redis_client()

    async def __call__(
        self, token: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]
    ) -> AuthToken:
        try:
            payload = jwt.decode(
                token.credentials, settings.jwt_public_key, algorithms=["RS256"]
            )
        except jwt.InvalidTokenError as e:
            raise credentials_exception from e

        if not payload.get("type") == self.token_type or not (
            sub := payload.get("sub")
        ):
            raise credentials_exception

        if await self.redis.exists(f"{DENYLIST_PREFIX}:{payload['jti']}"):
            raise credentials_exception

        if not await User.get(sub):
            raise credentials_exception

        return AuthToken(
            payload=payload, user_id=payload["sub"], encoded=token.credentials
        )
