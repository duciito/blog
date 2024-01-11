from pydantic import BaseModel, EmailStr, model_validator


class TokensSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class PasswordChangeSchema(BaseModel):
    current_password: str
    new_password: str

    @model_validator(mode="after")
    def check_passwords_are_not_equal(self):
        if self.current_password == self.new_password:
            raise ValueError("New password should not match the old one.")

        return self


class PasswordResetSchema(BaseModel):
    token: str
    password: str
