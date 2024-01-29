import base64
from functools import lru_cache

from fastapi_mail import ConnectionConfig
from pydantic import EmailStr, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongo_url: str
    password_salt: str

    # JWT auth related variables.
    jwt_sig_kid: str
    jwt_public_key: str
    jwt_private_key: str
    access_token_expiration: int
    refresh_token_expiration: int

    # AWS config
    aws_region: str = "eu-west-1"

    # Redis config
    redis_host: str
    redis_port: int
    redis_new_users_stream: str = "new-users"
    redis_likes_stream: str = "likes-stream"

    # SMTP credentials
    mail_username: str
    mail_password: str
    mail_host: str
    mail_port: int
    mail_from: EmailStr

    @field_validator("jwt_private_key", "jwt_public_key", mode="before")
    @classmethod
    def transform_jwt_keys(cls, encoded_key: str):
        return base64.b64decode(encoded_key)


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_email_config():
    settings = get_settings()

    return ConnectionConfig(
        MAIL_USERNAME=settings.mail_username,
        MAIL_PASSWORD=settings.mail_password,
        MAIL_FROM=settings.mail_from,
        MAIL_PORT=settings.mail_port,
        MAIL_SERVER=settings.mail_host,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
    )
