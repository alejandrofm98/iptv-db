"""Per-user movie and series library entries."""

import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class VodFavorite(Base):
    """A saved movie or series, independent of IPTV subscription state."""

    __tablename__ = "vod_favorites"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content_type: Mapped[str] = mapped_column(String(10), nullable=False)
    content_id: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "content_type", "content_id"),
        CheckConstraint("content_type IN ('movies', 'series')", name="ck_vod_favorites_type"),
        Index("ix_vod_favorites_user_created", "user_id", "created_at"),
    )
