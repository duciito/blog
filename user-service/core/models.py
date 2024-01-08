from datetime import UTC, datetime

from beanie import Document, Indexed
from pydantic import EmailStr, Field, validator

from core.utils import hash_password


class User(Document):
    email: Indexed(EmailStr, unique=True)
    password: str
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    profile_description: str | None
    joined_at: datetime = Field(default_factory=datetime.now)

    @validator("joined_at")
    def check_date_not_in_future(cls, val: datetime):
        if val.tzinfo is None or val.tzinfo.utcoffset(val) is None:
            val = val.replace(tzinfo=UTC)
        assert val < datetime.now().replace(tzinfo=UTC)
        return val

    def __repr__(self) -> str:
        return f"User: {self.email}"

    def check_password(self, password):
        return self.password == hash_password(password)

    async def set_password(self, password, save=False):
        self.password = hash_password(password)
        if save:
            await self.save()

    async def create(self, *args, **kwargs):
        # Override default create method to hash passwords for users.
        # IMPORTANT: this assumes the password has not already been hashed.
        await self.set_password(self.password)
        return await super().create(*args, **kwargs)
