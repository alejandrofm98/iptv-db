"""DB DTO for saved movies and series."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VodFavoriteDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    content_type: str
    content_id: str
    created_at: datetime
