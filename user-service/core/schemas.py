from pydantic import BaseModel, EmailStr, root_validator


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class PasswordChangeSchema(BaseModel):
    current_password: str
    new_password: str

    @root_validator
    def check_passwords_are_not_equal(cls, values):
        cp, np = values.values()

        if cp == np:
            raise ValueError('New password should not match the old one.')

        return values
