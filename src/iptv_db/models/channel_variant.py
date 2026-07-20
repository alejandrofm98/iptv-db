"""ChannelVariant model — quality variants per channel mapping."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from iptv_db.models.base import Base

if TYPE_CHECKING:
    from iptv_db.models.channel_mapping import ChannelMapping


class ChannelVariant(Base):
    """Quality variant for a channel mapping (FHD, HD, SD, 4K).

    Originally defined in walactv-scrapper schema as channel_variants table.
    """

    __tablename__ = "channel_variants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mapping_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("channel_mappings.id", ondelete="CASCADE"),
        nullable=False,
    )
    channel_id: Mapped[str | None] = mapped_column(
        String(50),
        ForeignKey("channels.id", ondelete="CASCADE"),
        nullable=True,
    )
    quality: Mapped[str | None] = mapped_column(Text, default="HD")
    priority: Mapped[int | None] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    mapping: Mapped[ChannelMapping] = relationship(back_populates="variants")
