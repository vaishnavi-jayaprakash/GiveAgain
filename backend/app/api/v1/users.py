from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
    Cookie,
    HTTPException
)

from sqlalchemy.orm import Session
from fastapi import Request

from app.core.rate_limit import limiter
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.db.database import get_db

from app.models import User

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.dependencies import get_current_user
from app.models.users import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserResponse, UserUpdateRequest
from app.services.user_service import UserService

user_router = APIRouter()


@user_router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user's profile",
)
def get_profile(
    current_user: User = Depends(get_current_user),
):
    """
    Returns the authenticated user's profile.
    """
    service = UserService(UserRepository(None))
    return service.get_profile(user=current_user)


@user_router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update current user's profile",
)
def update_profile(
    request: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the authenticated user's profile.
    Only fields provided in the request are updated.
    """
    service = UserService(
        UserRepository(db)
    )

    return service.update_profile(
        user=current_user,
        request=request,
    )