# app/models/listings.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    Float,
    DateTime,
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.enums import ListingCondition, ListingStatus

if TYPE_CHECKING:
    from .users import User
    from .categories import Category
    from .claims import Claim
    from .conversations import Conversation
    from .impact_records import ImpactRecord


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    donor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    condition: Mapped[ListingCondition] = mapped_column(
        Enum(ListingCondition),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    attributes: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    images: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    status: Mapped[ListingStatus] = mapped_column(
        Enum(ListingStatus),
        nullable=False,
        default=ListingStatus.AVAILABLE,
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

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    donor: Mapped["User"] = relationship(
        "User",
        back_populates="listings",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="listings",
    )

    claims: Mapped[list["Claim"]] = relationship(
        "Claim",
        back_populates="listing",
        cascade="all, delete-orphan",
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="listing",
        cascade="all, delete-orphan",
    )

    impact_records: Mapped[list["ImpactRecord"]] = relationship(
        "ImpactRecord",
        back_populates="listing",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Listing(id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status.value}')>"
        )