"""DB DTO for watch progress model."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WatchProgressDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    content_id: str
    content_type: str
    position_ms: int
    duration_ms: int
    series_name: str | None = None
    season_number: int | None = None
    episode_number: int | None = None
    title: str
    image_url: str
    last_watched_at: datetime | None = None
    is_watched: bool | None = None
