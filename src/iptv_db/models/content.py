"""Movie metadata, catalog, and stream models with concrete inheritance bases."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from iptv_db.models.base import Base

# ---------------------------------------------------------------------------
# Abstract bases for concrete inheritance (no table)
# ---------------------------------------------------------------------------


class MetadataBase(Base):
    """Columnas TMDB comunes para movies y series."""

    __abstract__ = True

    tmdb_id: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    original_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    overview_es: Mapped[str | None] = mapped_column(Text, nullable=True)
    overview_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    genres: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    vote_average: Mapped[float | None] = mapped_column(Float, nullable=True)
    vote_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    poster_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    backdrop_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    release_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tagline: Mapped[str | None] = mapped_column(String(500), nullable=True)
    popularity: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    imdb_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tmdb_data: Mapped[dict[str, object] | None] = mapped_column(JSONB, nullable=True)
    scraped_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class CatalogBase(Base):
    """Columnas comunes de catalogos IPTV para movies y series.

    Nota: tmdb_id se define en cada subclase con su FK correspondiente.
    """

    __abstract__ = True

    title: Mapped[str] = mapped_column(Text, nullable=False)
    provider_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nombre_dedup_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    canonical_key: Mapped[str | None] = mapped_column(String, nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    countries: Mapped[list[str] | None] = mapped_column(ARRAY(String(10)), nullable=True)
    group_normalizado: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now().astimezone()
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now().astimezone(),
        onupdate=lambda: datetime.now().astimezone(),
    )


class StreamBase(Base):
    """Columnas comunes de streams para movies y series."""

    __abstract__ = True

    country: Mapped[str] = mapped_column(String(10), nullable=False)
    quality: Mapped[str | None] = mapped_column(String(10), nullable=True)
    provider_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    stream_url: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)
    label: Mapped[str | None] = mapped_column(Text, nullable=True)
    numero: Mapped[int | None] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now().astimezone()
    )


# ---------------------------------------------------------------------------
# Concrete models
# ---------------------------------------------------------------------------


class MovieMetadata(MetadataBase):
    __tablename__ = "movies_metadata"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    runtime_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)


class MovieCatalog(CatalogBase):
    __tablename__ = "movies_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tmdb_id: Mapped[str | None] = mapped_column(
        String(20),
        ForeignKey("movies_metadata.tmdb_id", ondelete="SET NULL"),
        nullable=True,
    )

    metadata_row: Mapped["MovieMetadata | None"] = relationship(
        "MovieMetadata",
        primaryjoin="MovieCatalog.tmdb_id == MovieMetadata.tmdb_id",
        uselist=False,
    )
    streams: Mapped[list["MovieStream"]] = relationship(
        back_populates="movie", cascade="all, delete-orphan"
    )


class MovieStream(StreamBase):
    __tablename__ = "movie_streams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    movie_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("movies_catalog.id", ondelete="CASCADE"),
        nullable=False,
    )

    movie: Mapped["MovieCatalog"] = relationship(back_populates="streams")
