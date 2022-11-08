from pydantic import BaseModel, EmailStr


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
