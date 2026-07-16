from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.users import User
from app.models.enums import AccountType
from uuid import UUID

class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)

        return self.db.scalar(stmt)

    def get_by_id(self, user_id: UUID) -> User | None:
        stmt = select(User).where(User.id == user_id)

        return self.db.scalar(stmt)

    def create(
        self,
        *,
        email: str,
        hashed_password: str,
        account_type: AccountType,
        name: str,
        phone: str,
        locality: str,
        pincode: str,
        lat: float | None,
        lng: float | None,
    ) -> User:

        user = User(
            email=email,
            password_hash=hashed_password,
            account_type=account_type,
            name=name,
            phone=phone,
            locality=locality,
            pincode=pincode,
            lat=lat,
            lng=lng,
            is_email_verified=False,
            )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def update_password(self, user: User, new_hashed_password: str)-> User:
        user.password_hash = new_hashed_password
        self.db.commit()
        self.db.refresh(user)

        return user
    def save(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user