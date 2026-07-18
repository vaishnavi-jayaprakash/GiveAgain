from uuid import UUID

from fastapi import HTTPException, status 
from jose import JWTError

from app.repositories.user_repository import UserRepository

from app.models.users import User
from app.schemas.auth import UserUpdateRequest

class UserService:

    def __init__(self,repository: UserRepository):
        self.repository = repository

    def update_profile(self,*,user:User,request: UserUpdateRequest)->User:

        return self.repository.update_profile(
            user = user,
            data = request.model_dump(
                exclude_unset = True,
            ),
        )

