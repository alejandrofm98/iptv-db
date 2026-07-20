"""DB DTOs for channel models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ChannelDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    provider_id: str | None = None
    nombre: str
    nombre_normalizado: str | None = None
    logo: str | None = None
    grupo: str | None = None
    grupo_normalizado: str | None = None
    country: str | None = None
    url: str
    numero: int | None = None
    tvg_id: str | None = None
    created_at: datetime | None = None


class ChannelFavoriteDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: UUID
    channel_provider_id: str
    created_at: datetime
