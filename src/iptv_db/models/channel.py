"""Channel and channel favorites models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, PrimaryKeyConstraint, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class Channel(Base):
    """IPTV channel model.

    Legacy columns (added after initial ORM, exist in BD but not tracked before):
    - stream_url, ultimo_chequeo, estado_stream, tiempo_respuesta_ms, last_sync_at
    """

    __tablename__ = "channels"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    provider_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre_normalizado: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo: Mapped[str | None] = mapped_column(Text, nullable=True)
    grupo: Mapped[str | None] = mapped_column(String(255), nullable=True)
    grupo_normalizado: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(10), nullable=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    numero: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tvg_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Legacy columns — exist in BD, need to be in ORM for Alembic autogenerate alignment
    stream_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    ultimo_chequeo: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    estado_stream: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tiempo_respuesta_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    last_sync_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class ChannelFavorite(Base):
    __tablename__ = "channel_favorites"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    channel_provider_id: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now().astimezone()
    )

    __table_args__ = (PrimaryKeyConstraint("user_id", "channel_provider_id"),)
