"""DB DTOs for config and sync metadata."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConfigDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str | None = None
    description: str | None = None
    updated_at: datetime | None = None


class SyncMetadataDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    ultima_actualizacion: datetime | None = None
    total_canales: int | None = None
    total_movies: int | None = None
    total_series: int | None = None
    m3u_template_path: str | None = None
    m3u_template_filename: str | None = None
    m3u_size_mb: float | None = None
    channels_con_logo: int | None = None
    channels_sin_logo: int | None = None
    movies_con_logo: int | None = None
    movies_sin_logo: int | None = None
    series_con_logo: int | None = None
    series_sin_logo: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    channels_generated_at: datetime | None = None
    channels_json_size_mb: float | None = None
    movies_generated_at: datetime | None = None
    movies_json_size_mb: float | None = None
    series_generated_at: datetime | None = None
    series_json_size_mb: float | None = None
