# app/models/ngo_needs.py

from __future__ import annotations

import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Float,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.enums import NeedStatus

if TYPE_CHECKING:
    from .ngo_profiles import NGOProfile
    from .categories import Category


class NGONeed(Base):
    __tablename__ = "ngo_needs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    ngo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ngo_profiles.id", ondelete="CASCADE"),
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

    attributes: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    qty_needed: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    qty_claimed: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    deadline: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[NeedStatus] = mapped_column(
        Enum(NeedStatus),
        nullable=False,
        default=NeedStatus.PENDING,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    ngo_profile: Mapped["NGOProfile"] = relationship(
        "NGOProfile",
        back_populates="ngo_needs",
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="ngo_needs",
    )

    def __repr__(self) -> str:
        return (
            f"<NGONeed(id={self.id}, "
            f"title='{self.title}', "
            f"status='{self.status.value}')>"
        )