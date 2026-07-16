from app.schemas.auth import SignupRequest
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.core.config import settings
from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.repositories.user_repository import UserRepository

from app.services.auth_service import AuthService

from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    MessageResponse,
)
from app.api.v1.auth import router as auth_router

print(auth_router)

print(settings.ALGORITHM)