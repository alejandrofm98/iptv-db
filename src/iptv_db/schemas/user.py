"""DB DTOs for user and session models."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    password_hash: str
    max_connections: int | None = None
    is_active: bool | None = None
    role: str | None = None
    expires_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class ActiveSessionDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    device_id: str
    device_name: str | None = None
    device_type: str | None = None
    ip_address: str | None = None
    user_agent: str | None = None
    last_activity: datetime | None = None
    created_at: datetime | None = None
