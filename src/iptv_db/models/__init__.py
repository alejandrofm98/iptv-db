"""All ORM models for iptv-db."""

from iptv_db.models.base import Base
from iptv_db.models.calendario import Calendario
from iptv_db.models.channel import Channel, ChannelFavorite
from iptv_db.models.channel_mapping import ChannelMapping
from iptv_db.models.channel_variant import ChannelVariant
from iptv_db.models.config import Config, SyncMetadata
from iptv_db.models.content import MovieCatalog, MovieMetadata, MovieStream
from iptv_db.models.replay import Replay
from iptv_db.models.scraper import ScraperFailure
from iptv_db.models.series import SeriesCatalog, SeriesEpisode, SeriesMetadata, SeriesStream
from iptv_db.models.user import ActiveSession, User
from iptv_db.models.watch_progress import WatchProgress

__all__ = [
    "ActiveSession",
    "Base",
    "Calendario",
    "Channel",
    "ChannelFavorite",
    "ChannelMapping",
    "ChannelVariant",
    "Config",
    "MovieCatalog",
    "MovieMetadata",
    "MovieStream",
    "Replay",
    "ScraperFailure",
    "SeriesCatalog",
    "SeriesEpisode",
    "SeriesMetadata",
    "SeriesStream",
    "SyncMetadata",
    "User",
    "WatchProgress",
]
