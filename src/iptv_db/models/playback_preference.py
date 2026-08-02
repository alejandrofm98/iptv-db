"""Preferencias de audio y subtitulos por usuario y contenido."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class PlaybackPreference(Base):
    __tablename__ = "playback_preferences"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    catalog_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    audio_language: Mapped[str | None] = mapped_column(String(32), nullable=True)
    audio_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subtitle_language: Mapped[str | None] = mapped_column(String(32), nullable=True)
    subtitle_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subtitles_disabled: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint(
            "content_type IN ('movie', 'series')",
            name="ck_playback_preferences_content_type",
        ),
        UniqueConstraint(
            "user_id",
            "content_type",
            "catalog_id",
            name="uq_playback_preferences_user_content",
        ),
    )
