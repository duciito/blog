from datetime import datetime, timezone
from typing import Optional

from beanie import Document, Indexed
from pydantic import EmailStr, Field, validator

from core.utils import hash_password


class User(Document):
    email: Indexed(EmailStr, unique=True)
    password: str
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    profile_description: Optional[str]
    joined_at: datetime = Field(default_factory=datetime.now)

    @validator('joined_at')
    def check_date_not_in_future(cls, val: datetime):
        assert val < datetime.now().replace(tzinfo=timezone.utc)
        return val

    def __repr__(self) -> str:
        return f"User: {self.email}"

    async def create(self, *args, **kwargs):
        # Override default create method to hash passwords for users.
        self.password = hash_password(self.password)
        return await super().create(*args, **kwargs)
