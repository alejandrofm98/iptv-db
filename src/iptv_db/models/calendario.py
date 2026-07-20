"""Calendario model — sports calendar table from walactv-scrapper."""

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class Calendario(Base):
    """Sports event calendar table, originally defined in walactv-scrapper schema."""

    __tablename__ = "calendario"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    hora: Mapped[str] = mapped_column(Text, nullable=False)
    competicion: Mapped[str | None] = mapped_column(Text, nullable=True)
    subtitulo_competicion: Mapped[str | None] = mapped_column(Text, nullable=True)
    categoria: Mapped[str | None] = mapped_column(Text, nullable=True)
    equipos: Mapped[str] = mapped_column(Text, nullable=False)
    imagen_evento: Mapped[str | None] = mapped_column(Text, nullable=True)
    canales: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        UniqueConstraint("fecha", "hora", "equipos", name="uq_calendario_fecha_hora_equipos"),
    )
