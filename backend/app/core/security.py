from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS

EMAIL_VERIFICATION_EXPIRE_HOURS = 24
PASSWORD_RESET_EXPIRE_MINUTES = 30


# ------------------------------------------------------------------
# Password Helpers
# ------------------------------------------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ------------------------------------------------------------------
# Generic Token Creator
# ------------------------------------------------------------------

def create_token(
    *,
    data: dict[str, Any],
    token_type: str,
    expires_delta: timedelta,
) -> str:
    payload = data.copy()

    payload.update(
        {
            "type": token_type,
            "exp": datetime.now(timezone.utc) + expires_delta,
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ------------------------------------------------------------------
# Access Token
# ------------------------------------------------------------------

def create_access_token(data: dict[str, Any]) -> str:
    return create_token(
        data=data,
        token_type="access",
        expires_delta=timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )


# ------------------------------------------------------------------
# Refresh Token
# ------------------------------------------------------------------

def create_refresh_token(data: dict[str, Any]) -> str:
    return create_token(
        data=data,
        token_type="refresh",
        expires_delta=timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        ),
    )


# ------------------------------------------------------------------
# Email Verification Token
# ------------------------------------------------------------------

def create_email_verification_token(
    data: dict[str, Any],
) -> str:
    return create_token(
        data=data,
        token_type="email_verification",
        expires_delta=timedelta(
            hours=EMAIL_VERIFICATION_EXPIRE_HOURS
        ),
    )


# ------------------------------------------------------------------
# Password Reset Token
# ------------------------------------------------------------------

def create_reset_token(
    data: dict[str, Any],
) -> str:
    return create_token(
        data=data,
        token_type="password_reset",
        expires_delta=timedelta(
            minutes=PASSWORD_RESET_EXPIRE_MINUTES
        ),
    )


# ------------------------------------------------------------------
# Decode Token
# ------------------------------------------------------------------

def decode_token(
    token: str,
) -> dict[str, Any]:
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

def create_email_verification_token(data: dict) -> str:
    """
    Create a JWT token for email verification.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(hours=24)

    payload.update(
        {
            "exp": expire,
            "type": "email_verification",
        }
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )