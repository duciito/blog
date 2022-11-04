from functools import lru_cache
from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    mongo_url: MongoDsn
    password_salt: str


@lru_cache
def get_settings():
    return Settings()
