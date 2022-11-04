from functools import lru_cache
from pydantic import BaseSettings, MongoDsn


class Settings(BaseSettings):
    mongo_host: MongoDsn
    mongo_port: int = 27017


@lru_cache
def get_settings():
    return Settings()
