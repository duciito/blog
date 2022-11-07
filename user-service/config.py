from functools import lru_cache
from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    mongo_url: MongoDsn
    password_salt: str

    # JWT auth related variables.
    jwt_public_key: str
    jwt_private_key: str
    jwt_algorithm: str
    access_token_expiration: int
    refresh_token_expiration: int


@lru_cache
def get_settings():
    return Settings()
