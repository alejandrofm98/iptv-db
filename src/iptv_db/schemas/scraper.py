"""DB DTO for scraper failures."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ScraperFailureDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    provider_id: str | None = None
    series_key: str | None = None
    title: str
    year: int | None = None
    error_message: str | None = None
    failed_at: datetime | None = None
    retry_count: int | None = None
    last_retry_at: datetime | None = None
