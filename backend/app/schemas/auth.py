import re
from typing import Annotated

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    HttpUrl
)

from app.models.enums import AccountType


# --------------------------------------------------
# Reusable Password Type
# --------------------------------------------------

Password = Annotated[
    str,
    Field(
        min_length=8,
        max_length=128,
    ),
]


# --------------------------------------------------
# Signup
# --------------------------------------------------

class SignupRequest(BaseModel):
    email: EmailStr
    password: Password
    account_type: AccountType

    name: str
    phone: str
    locality: Annotated[str | None,Field(min_length=2, max_length=255),] = None


    pincode: str

    lat: Annotated[float | None,Field(ge=-90, le=90),] = None
    lng:  Annotated[float | None,Field(ge=-180, le=180),] = None

    # NGO-only fields
    dharpan_id: str | None = None
    cert_doc_url: str | None = None
    reg_doc_url: str | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.fullmatch(r"^[6-9]\d{9}$", value):
            raise ValueError("Invalid phone number")
        return value

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value: str) -> str:
        if not re.fullmatch(r"^\d{6}$", value):
            raise ValueError("Invalid pincode")
        return value
    
   
# --------------------------------------------------
# Login
# --------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: Password


# --------------------------------------------------
# Token Responses
# --------------------------------------------------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --------------------------------------------------
# Forgot Password
# --------------------------------------------------

class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# --------------------------------------------------
# Change Password
# --------------------------------------------------

class ChangePasswordRequest(BaseModel):
    current_password: Password
    new_password: Password


# --------------------------------------------------
# Reset Password
# --------------------------------------------------

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: Password


# --------------------------------------------------
# Generic Message Response
# --------------------------------------------------

class MessageResponse(BaseModel):
    message: str


# --------------------------------------------------
# Update Logged-in User
# --------------------------------------------------

class UserUpdateRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
    locality: Annotated[str | None,Field(min_length=2, max_length=255),] = None
    pincode: str | None = None
    lat: Annotated[float | None,Field(ge=-90, le=90),] = None
    lng:  Annotated[float | None,Field(ge=-180, le=180),] = None
    profile_photo_url: HttpUrl | None = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is None:
            return value

        if not re.fullmatch(r"^[6-9]\d{9}$", value):
            raise ValueError("Invalid phone number")

        return value

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value: str | None) -> str | None:
        if value is None:
            return value

        if not re.fullmatch(r"^\d{6}$", value):
            raise ValueError("Invalid pincode")

        return value


# --------------------------------------------------
# User Response
# --------------------------------------------------

class UserResponse(BaseModel):
    id: str
    email: EmailStr

    account_type: AccountType

    name: str
    phone: str
    locality: str
    pincode: str

    lat: float | None
    lng: float | None

    profile_photo_url: HttpUrl | None

    is_email_verified: bool

    model_config = {
        "from_attributes": True,
    }