import hashlib

from config import get_settings


def hash_password(password: str):
    """Returns a salted password hash."""
    settings = get_settings()
    return hashlib.sha512(
        password.encode() + settings.password_salt.encode()
    ).hexdigest()
