# app/models/users.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Boolean,
    Float,
    DateTime,
    Enum,
    Integer,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.enums import AccountType

if TYPE_CHECKING:
    from .ngo_profiles import NGOProfile
    from .listings import Listing
    from .notifications import Notification
    from .conversations import Conversation
    from .messages import Message
    from .impact_records import ImpactRecord


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
    )

    account_type: Mapped[AccountType] = mapped_column(
        Enum(AccountType),
        nullable=False,
    )

    locality: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    pincode: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    lat: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    lng: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    is_email_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    reset_token_version: Mapped[int] = mapped_column(
    Integer,
    default=0,
    nullable=False,
)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    ngo_profile: Mapped["NGOProfile | None"] = relationship(
        "NGOProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    listings: Mapped[list["Listing"]] = relationship(
        "Listing",
        back_populates="donor",
        cascade="all, delete-orphan",
    )

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    donor_conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        foreign_keys="Conversation.donor_id",
        back_populates="donor",
        cascade="all, delete-orphan",
    )

    ngo_conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        foreign_keys="Conversation.ngo_id",
        back_populates="ngo",
        cascade="all, delete-orphan",
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="sender",
        cascade="all, delete-orphan",
    )

    impact_records: Mapped[list["ImpactRecord"]] = relationship(
        "ImpactRecord",
        back_populates="donor",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"