# app/models/impact_records.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Float,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from .users import User
    from .listings import Listing
    from .claims import Claim


class ImpactRecord(Base):
    __tablename__ = "impact_records"

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

    listing_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("listings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    claim_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("claims.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,      # One Claim -> One Impact Record
        index=True,
    )

    est_weight_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    certificate_url: Mapped[str | None] = mapped_column(
        String(500),
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
        back_populates="impact_records",
    )

    listing: Mapped["Listing"] = relationship(
        "Listing",
        back_populates="impact_records",
    )

    claim: Mapped["Claim"] = relationship(
        "Claim",
        back_populates="impact_record",
        uselist=False,
    )

    def __repr__(self) -> str:
        return (
            f"<ImpactRecord(id={self.id}, "
            f"claim_id={self.claim_id}, "
            f"weight={self.est_weight_kg}kg)>"
        )