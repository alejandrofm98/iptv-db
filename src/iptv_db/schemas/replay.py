"""DB DTO for replay model."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReplayDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    source_site: str
    title: str
    event_name: str | None = None
    event_type: str | None = None
    event_date: datetime | None = None
    post_url: str
    featured_image_url: str | None = None
    description: str | None = None
    video_sources: dict[str, object]
    match_card: dict[str, object]
    created_at: datetime | None = None
    updated_at: datetime | None = None
