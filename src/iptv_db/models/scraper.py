"""Scraper failure tracking model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class ScraperFailure(Base):
    __tablename__ = "scraper_failures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    series_key: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now().astimezone()
    )
    retry_count: Mapped[int | None] = mapped_column(Integer, default=1)
    last_retry_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now().astimezone()
    )

    __table_args__ = (
        Index(
            "idx_failures_provider",
            "provider_id",
            unique=True,
            postgresql_where=text("provider_id IS NOT NULL"),
        ),
        Index(
            "idx_failures_series",
            "series_key",
            unique=True,
            postgresql_where=text("series_key IS NOT NULL"),
        ),
    )
