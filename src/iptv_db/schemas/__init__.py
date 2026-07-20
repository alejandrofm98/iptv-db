"""DB DTOs re-exports."""

from iptv_db.schemas.channel import ChannelDB, ChannelFavoriteDB
from iptv_db.schemas.config import ConfigDB, SyncMetadataDB
from iptv_db.schemas.content import MovieCatalogDB, MovieMetadataDB, MovieStreamDB
from iptv_db.schemas.replay import ReplayDB
from iptv_db.schemas.scraper import ScraperFailureDB
from iptv_db.schemas.series import (
    SeriesCatalogDB,
    SeriesEpisodeDB,
    SeriesMetadataDB,
    SeriesStreamDB,
)
from iptv_db.schemas.user import ActiveSessionDB, UserDB
from iptv_db.schemas.watch_progress import WatchProgressDB

__all__ = [
    "ActiveSessionDB",
    "ChannelDB",
    "ChannelFavoriteDB",
    "ConfigDB",
    "MovieCatalogDB",
    "MovieMetadataDB",
    "MovieStreamDB",
    "ReplayDB",
    "ScraperFailureDB",
    "SeriesCatalogDB",
    "SeriesEpisodeDB",
    "SeriesMetadataDB",
    "SeriesStreamDB",
    "SyncMetadataDB",
    "UserDB",
    "WatchProgressDB",
]
