"""Persisted metadata imported from external Stremio catalogs."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from iptv_db.models.base import Base


class ExternalCatalogItem(Base):
    """Ficha de Cinemeta independiente de cualquier proveedor IPTV."""

    __tablename__ = "external_catalog_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_type: Mapped[str] = mapped_column(String(10), nullable=False)
    catalog_id: Mapped[str] = mapped_column(String(50), nullable=False)
    catalog_position: Mapped[int] = mapped_column(Integer, nullable=False)
    imdb_id: Mapped[str] = mapped_column(String(20), nullable=False)
    moviedb_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    title_es: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    overview_es: Mapped[str | None] = mapped_column(Text, nullable=True)
    poster: Mapped[str | None] = mapped_column(Text, nullable=True)
    backdrop: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    imported_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now().astimezone()
    )
    last_seen_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now().astimezone()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now().astimezone(),
        onupdate=lambda: datetime.now().astimezone(),
    )

    __table_args__ = (
        UniqueConstraint(
            "content_type",
            "catalog_id",
            "imdb_id",
            name="uq_external_catalog_items_identity",
        ),
        Index("ix_external_catalog_items_type_catalog", "content_type", "catalog_id"),
        Index(
            "ix_external_catalog_items_type_imdb_id",
            "content_type",
            "imdb_id",
        ),
        Index(
            "ix_external_catalog_items_type_catalog_position",
            "content_type",
            "catalog_id",
            "catalog_position",
        ),
    )
