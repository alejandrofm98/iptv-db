"""Watch progress model for tracking user viewing progress."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class WatchProgress(Base):
    __tablename__ = "watch_progress"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    content_id: Mapped[str] = mapped_column(String(100), nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    position_ms: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    duration_ms: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    series_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    season_number: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    episode_number: Mapped[int | None] = mapped_column(Integer, nullable=True, default=0)
    title: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    image_url: Mapped[str] = mapped_column(String, nullable=False, default="")
    last_watched_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    is_watched: Mapped[bool | None] = mapped_column(Boolean, nullable=False, default=False)

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "content_id",
            "season_number",
            "episode_number",
            name="watch_progress_user_content_unique",
            postgresql_nulls_not_distinct=True,
        ),
    )
