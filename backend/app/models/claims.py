# app/models/claims.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.enums import ClaimStatus

if TYPE_CHECKING:
    from .ngo_profiles import NGOProfile
    from .listings import Listing
    from .impact_records import ImpactRecord


class Claim(Base):
    __tablename__ = "claims"

    __table_args__ = (
        UniqueConstraint(
            "listing_id",
            "ngo_id",
            name="uq_claim_listing_ngo",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    listing_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("listings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    ngo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("ngo_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[ClaimStatus] = mapped_column(
        Enum(ClaimStatus),
        nullable=False,
        default=ClaimStatus.PENDING,
    )

    claimed_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    listing: Mapped["Listing"] = relationship(
        "Listing",
        back_populates="claims",
    )

    ngo_profile: Mapped["NGOProfile"] = relationship(
        "NGOProfile",
        back_populates="claims",
    )

    impact_record: Mapped["ImpactRecord | None"] = relationship(
        "ImpactRecord",
        back_populates="claim",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Claim(id={self.id}, "
            f"listing_id={self.listing_id}, "
            f"status='{self.status.value}')>"
        )