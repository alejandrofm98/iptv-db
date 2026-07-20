"""DB DTOs for movie metadata, catalog, and stream models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MovieMetadataDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tmdb_id: str | None = None
    title: str | None = None
    original_title: str | None = None
    overview_es: str | None = None
    overview_en: str | None = None
    genres: list[str] | None = None
    vote_average: float | None = None
    vote_count: int | None = None
    poster_path: str | None = None
    backdrop_path: str | None = None
    release_date: datetime | None = None
    year: int | None = None
    runtime_minutes: int | None = None
    tagline: str | None = None
    popularity: float | None = None
    status: str | None = None
    imdb_id: str | None = None
    tmdb_data: dict[str, object] | None = None
    scraped_at: datetime | None = None
    updated_at: datetime | None = None


class MovieCatalogDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    provider_id: str | None = None
    tmdb_id: str | None = None
    nombre_dedup_key: str | None = None
    canonical_key: str | None = None
    year: int | None = None
    countries: list[str] | None = None
    group_normalizado: str | None = None
    logo: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class MovieStreamDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    movie_id: UUID
    country: str
    quality: str | None = None
    provider_id: str | None = None
    stream_url: str
    url: str | None = None
    label: str | None = None
    numero: int | None = None
    created_at: datetime | None = None
