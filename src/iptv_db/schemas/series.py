"""DB DTOs for series models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SeriesMetadataDB(BaseModel):
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
    tagline: str | None = None
    popularity: float | None = None
    status: str | None = None
    imdb_id: str | None = None
    tmdb_data: dict[str, object] | None = None
    scraped_at: datetime | None = None
    updated_at: datetime | None = None


class SeriesCatalogDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    series_key: str
    canonical_key: str | None = None
    provider_id: str | None = None
    tmdb_id: str | None = None
    nombre_dedup_key: str | None = None
    year: int | None = None
    countries: list[str] | None = None
    group_normalizado: str | None = None
    logo: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class SeriesEpisodeDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    catalog_id: UUID
    season_number: int
    episode_number: int
    title: str | None = None
    overview: str | None = None
    air_date: datetime | None = None
    still_path: str | None = None
    numero: int | None = None
    title_en: str | None = None
    overview_en: str | None = None
    runtime: int | None = None
    vote_average: float | None = None
    vote_count: int | None = None
    episode_type: str | None = None
    tmdb_checked: bool | None = None


class SeriesStreamDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    episode_id: UUID
    country: str
    quality: str | None = None
    provider_id: str | None = None
    stream_url: str
    url: str | None = None
    label: str | None = None
    numero: int | None = None
    created_at: datetime | None = None
