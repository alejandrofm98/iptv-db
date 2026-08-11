"""Skip segments cached from external providers."""

import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class VideoSegmentSync(Base):
    """Estado de sincronización por episodio y fuente."""

    __tablename__ = "video_segment_sync"

    episode_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("series_episodes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    source: Mapped[str] = mapped_column(String(30), primary_key=True)
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    not_found: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class VideoSegment(Base):
    """Intervalo omitible de un episodio."""

    __tablename__ = "video_segments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    episode_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("series_episodes.id", ondelete="CASCADE"),
        nullable=False,
    )
    segment_type: Mapped[str] = mapped_column(String(10), nullable=False)
    start_ms: Mapped[int] = mapped_column(BigInteger, nullable=False)
    end_ms: Mapped[int] = mapped_column(BigInteger, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Numeric(4, 3), nullable=True)
    submission_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String(30), nullable=False)
    source_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (UniqueConstraint("episode_id", "segment_type", "source"),)
