# app/models/categories.py

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from .listings import Listing
    from .ngo_needs import NGONeed


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    slug: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
    )

    # Defines the dynamic attributes for this category.
    # Example:
    # {
    #   "brand": "string",
    #   "expiry_date": "date",
    #   "size": "string"
    # }
    attribute_schema: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    # ---------------------------------
    # Relationships
    # ---------------------------------

    listings: Mapped[list["Listing"]] = relationship(
        "Listing",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    ngo_needs: Mapped[list["NGONeed"]] = relationship(
        "NGONeed",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Category(id={self.id}, "
            f"name='{self.name}')>"
        )