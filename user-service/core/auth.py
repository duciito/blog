import base64

from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT
from config import get_settings

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
