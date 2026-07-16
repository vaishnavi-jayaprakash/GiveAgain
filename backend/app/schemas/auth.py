from typing import Annotated

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.models.enums import AccountType


Password = Annotated[
    str,
    Field(
        min_length=8,
        max_length=128,
    ),
]


class SignupRequest(BaseModel):
    email: EmailStr
    password: Password
    account_type: AccountType
    phone: str
    pincode: str
    name: str
    locality: str
    lat: float | None = None
    lng: float | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: Password


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ChangePasswordRequest(BaseModel):
    current_password: Password
    new_password: Password


class MessageResponse(BaseModel):
    message: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: Password