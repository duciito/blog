import base64
from datetime import timedelta

from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from config import get_settings
from core.models import User
from core.schemas import TokensSchema

settings = get_settings()


class AuthSettings(BaseModel):
    authjwt_algorithm: str = settings.jwt_algorithm
    authjwt_public_key: str = base64.b64decode(
            settings.jwt_public_key).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
            settings.jwt_private_key).decode('utf-8')


@AuthJWT.load_config
def get_config():
    return AuthSettings()


def create_tokens(user: User) -> TokensSchema:
    auth = AuthJWT()
    access_token = auth.create_access_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=settings.access_token_expiration)
    )
    refresh_token = auth.create_refresh_token(
        subject=str(user.id),
        expires_time=timedelta(minutes=settings.refresh_token_expiration)
    )
    return TokensSchema(access_token=access_token, refresh_token=refresh_token)
