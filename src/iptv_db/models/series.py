"""Series metadata, catalog, episode and stream models."""

import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from iptv_db.models.base import Base
from iptv_db.models.content import MetadataBase, StreamBase


class SeriesMetadata(MetadataBase):
    __tablename__ = "series_metadata"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


class SeriesCatalog(Base):
    __tablename__ = "series_catalog"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    series_key: Mapped[str] = mapped_column(Text, nullable=False)
    canonical_key: Mapped[str | None] = mapped_column(String, nullable=True)
    provider_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tmdb_id: Mapped[str | None] = mapped_column(
        String(20),
        ForeignKey("series_metadata.tmdb_id", ondelete="SET NULL"),
        nullable=True,
    )
    nombre_dedup_key: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    metadata_row: Mapped["SeriesMetadata | None"] = relationship(
        "SeriesMetadata",
        primaryjoin="SeriesCatalog.tmdb_id == SeriesMetadata.tmdb_id",
        uselist=False,
    )
    episodes: Mapped[list["SeriesEpisode"]] = relationship(
        back_populates="catalog", cascade="all, delete-orphan"
    )


class SeriesEpisode(Base):
    __tablename__ = "series_episodes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    catalog_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("series_catalog.id", ondelete="CASCADE"),
        nullable=False,
    )
    season_number: Mapped[int] = mapped_column(Integer, nullable=False)
    episode_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    overview: Mapped[str | None] = mapped_column(Text, nullable=True)
    air_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    still_path: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero: Mapped[int | None] = mapped_column(Integer, nullable=True)
    title_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    overview_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    runtime: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vote_average: Mapped[float | None] = mapped_column(Float, nullable=True)
    vote_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    episode_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tmdb_checked: Mapped[bool | None] = mapped_column(Boolean, default=False)

    __table_args__ = (UniqueConstraint("catalog_id", "season_number", "episode_number"),)

    catalog: Mapped["SeriesCatalog"] = relationship(back_populates="episodes")
    streams: Mapped[list["SeriesStream"]] = relationship(
        back_populates="episode", cascade="all, delete-orphan"
    )


class SeriesStream(StreamBase):
    __tablename__ = "series_streams"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    episode_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("series_episodes.id", ondelete="CASCADE"),
        nullable=False,
    )

    episode: Mapped["SeriesEpisode"] = relationship(back_populates="streams")
