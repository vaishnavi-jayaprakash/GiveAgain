# app/models/ngo_profiles.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    DateTime,
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.enums import VerificationStatus

if TYPE_CHECKING:
    from .users import User
    from .ngo_needs import NGONeed
    from .claims import Claim


class NGOProfile(Base):
    __tablename__ = "ngo_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,          # One User -> One NGO Profile
        index=True,
    )

    dharpan_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    cert_doc_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    reg_doc_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    verification_status: Mapped[VerificationStatus] = mapped_column(
        Enum(VerificationStatus),
        nullable=False,
        default=VerificationStatus.PENDING,
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    verified_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ------------------------
    # Relationships
    # ------------------------

    user: Mapped["User"] = relationship(
        "User",
        back_populates="ngo_profile",
    )

    ngo_needs: Mapped[list["NGONeed"]] = relationship(
        "NGONeed",
        back_populates="ngo_profile",
        cascade="all, delete-orphan",
    )

    claims: Mapped[list["Claim"]] = relationship(
        "Claim",
        back_populates="ngo_profile",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<NGOProfile(id={self.id}, "
            f"dharpan_id='{self.dharpan_id}', "
            f"status='{self.verification_status.value}')>"
        )