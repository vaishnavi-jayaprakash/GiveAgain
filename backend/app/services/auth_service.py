from uuid import UUID

from fastapi import HTTPException, status
from jose import JWTError

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
)

from app.models.enums import AccountType
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.core.security import create_email_verification_token

class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    # --------------------------------------------------
    # Signup
    # --------------------------------------------------

    def signup(
        self,
        *,
        email: str,
        password: str,
        account_type: AccountType,
        name: str,
        phone: str,
        locality: str,
        pincode: str,
        lat: float | None,
        lng: float | None,
    ) -> User:

        existing = self.repository.get_by_email(email)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        password_hash = hash_password(password)

        user = self.repository.create(
            email=email,
            hashed_password=password_hash,
            account_type=account_type,
            name=name,
            phone=phone,
            locality=locality,
            pincode=pincode,
            lat=lat,
            lng=lng,
        )
        verification_token = create_email_verification_token(
        {
            "sub": str(user.id)
        }
        )

        print(
            f"http://localhost:5173/verify-email?token={verification_token}"
        )
        return user

    # --------------------------------------------------
    # Login
    # --------------------------------------------------

    def login(
        self,
        *,
        email: str,
        password: str,
    ):

        user = self.repository.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        if not user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please verify your email before logging in.",
            )
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.account_type.value,
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id),
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    # --------------------------------------------------
    # Refresh Access Token
    # --------------------------------------------------

    def refresh(
        self,
        refresh_token: str,
    ) -> str:

        try:
            payload = decode_token(refresh_token)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

        user = self.repository.get_by_id(
            UUID(payload["sub"])
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.account_type.value,
            }
        )

    # --------------------------------------------------
    # Generate Password Reset Token
    # --------------------------------------------------

    def generate_reset_token(
        self,
        email: str,
    ) -> str | None:

        user = self.repository.get_by_email(email)

        if user is None:
            return None

        return create_reset_token(
            {
                "sub": str(user.id),
                "version": user.reset_token_version,
            }
        )

    # --------------------------------------------------
    # Reset Password
    # --------------------------------------------------

    def reset_password(
        self,
        *,
        reset_token: str,
        new_password: str,
    ) -> None:

        try:
            payload = decode_token(reset_token)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        if payload.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid reset token",
            )

        user = self.repository.get_by_id(
            UUID(payload["sub"])
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if payload["version"] != user.reset_token_version:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Reset token has already been used",
            )

        password_hash = hash_password(new_password)

        self.repository.update_password(
            user=user,
            new_hashed_password=password_hash,
        )

        user.reset_token_version += 1
        self.repository.save(user)

    # --------------------------------------------------
    # Change Password (Authenticated User)
    # --------------------------------------------------

    def change_password(
        self,
        *,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:

        if not verify_password(
            current_password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Current password is incorrect",
            )

        password_hash = hash_password(new_password)

        self.repository.update_password(
            user=user,
            new_hashed_password=password_hash,
        )

    def verify_email(
    self,
    token: str,
):

        try:
            payload = decode_token(token)

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired verification token",
            )

        if payload.get("type") != "email_verification":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid verification token",
            )

        user = self.repository.get_by_id(
            UUID(payload["sub"])
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.is_email_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already verified.",
            )

        user.is_email_verified = True

        self.repository.save(user)