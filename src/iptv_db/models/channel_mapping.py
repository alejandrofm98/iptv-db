"""ChannelMapping model — maps scrapper source names to display names."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from iptv_db.models.base import Base

if TYPE_CHECKING:
    from iptv_db.models.channel_variant import ChannelVariant


class ChannelMapping(Base):
    """Maps a source channel name (from scrapper) to a display name.

    Originally defined in walactv-scrapper schema as channel_mappings table.
    """

    __tablename__ = "channel_mappings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    variants: Mapped[list[ChannelVariant]] = relationship(
        back_populates="mapping", cascade="all, delete-orphan"
    )
