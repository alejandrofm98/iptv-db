"""Config and sync metadata models."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class Config(Base):
    __tablename__ = "config"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now().astimezone()
    )


class SyncMetadata(Base):
    __tablename__ = "sync_metadata"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    ultima_actualizacion: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    total_canales: Mapped[int | None] = mapped_column(Integer, nullable=True, server_default="0")
    total_movies: Mapped[int | None] = mapped_column(Integer, nullable=True, server_default="0")
    total_series: Mapped[int | None] = mapped_column(Integer, nullable=True, server_default="0")
    m3u_template_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    m3u_template_filename: Mapped[str | None] = mapped_column(Text, nullable=True)
    m3u_size_mb: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    channels_con_logo: Mapped[int | None] = mapped_column(
        Integer, nullable=True, server_default="0"
    )
    channels_sin_logo: Mapped[int | None] = mapped_column(
        Integer, nullable=True, server_default="0"
    )
    movies_con_logo: Mapped[int | None] = mapped_column(Integer, nullable=True, server_default="0")
    movies_sin_logo: Mapped[int | None] = mapped_column(Integer, nullable=True, server_default="0")
    series_con_logo: Mapped[int | None] = mapped_column(Integer, nullable=True, server_default="0")
    series_sin_logo: Mapped[int | None] = mapped_column(Integer, nullable=True, server_default="0")
    created_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    channels_generated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    channels_json_size_mb: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    movies_generated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    movies_json_size_mb: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    series_generated_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    series_json_size_mb: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
