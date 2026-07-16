from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    Cookie,
    HTTPException,
)

from sqlalchemy.orm import Session
from fastapi import Request

from app.core.rate_limit import limiter
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.db.database import get_db

from app.models.users import User

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    RefreshResponse,
    MessageResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# --------------------------------------------------
# Signup
# --------------------------------------------------

@router.post(
    "/signup",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/15minutes")
def signup(
    request: SignupRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(UserRepository(db))

    service.signup(
        email=request.email,
        password=request.password,
        account_type=request.account_type,
        name=request.name,
        phone=request.phone,
        locality=request.locality,
        pincode=request.pincode,
        lat=request.lat,
        lng=request.lng,
    )

    return {"message": "User created successfully."}


# --------------------------------------------------
# Login
# --------------------------------------------------

@router.post(
    "/login",
    response_model=TokenResponse,
)
@limiter.limit("5/15minutes")
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    service = AuthService(UserRepository(db))

    tokens = service.login(
        email=request.email,
        password=request.password,
    )

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )

    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer",
    }


# --------------------------------------------------
# Refresh
# --------------------------------------------------

@router.post(
    "/refresh",
    response_model=RefreshResponse,
)
def refresh(
    refresh_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing refresh token",
        )

    service = AuthService(UserRepository(db))

    access_token = service.refresh(refresh_token)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# --------------------------------------------------
# Logout
# --------------------------------------------------

@router.post(
    "/logout",
    response_model=MessageResponse,
)
def logout(
    response: Response,
):
    response.delete_cookie("refresh_token")

    return {
        "message": "Logged out successfully."
    }


# --------------------------------------------------
# Current User
# --------------------------------------------------

@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user


# --------------------------------------------------
# Forgot Password
# --------------------------------------------------

@router.post(
    "/forgot-password",
    response_model=MessageResponse,
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(
        UserRepository(db)
    )

    token = service.generate_reset_token(
        request.email
    )

    if token:
        print(
            f"http://localhost:5173/reset-password?token={token}"
        )

    return {
        "message":
        "If an account exists, a reset link has been generated."
    }


# --------------------------------------------------
# Reset Password
# --------------------------------------------------

@router.post(
    "/reset-password",
    response_model=MessageResponse,
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(
        UserRepository(db)
    )

    service.reset_password(
        reset_token=request.token,
        new_password=request.new_password,
    )

    return {
        "message":
        "Password reset successfully."
    }


# --------------------------------------------------
# Change Password
# --------------------------------------------------

@router.post(
    "/change-password",
    response_model=MessageResponse,
)
def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AuthService(UserRepository(db))

    service.change_password(
        user=current_user,
        current_password=request.current_password,
        new_password=request.new_password,
    )

    return {
        "message": "Password changed successfully."
    }

@router.get(
    "/verify-email/{token}",
    response_model=MessageResponse,
)
def verify_email(
    token: str,
    db: Session = Depends(get_db),
):

    service = AuthService(
        UserRepository(db)
    )

    service.verify_email(token)

    return {
        "message": "Email verified successfully."
    }