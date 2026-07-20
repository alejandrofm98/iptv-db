"""Verify the package can be imported and models are registered."""


def test_base_imports() -> None:
    from iptv_db.models import (  # noqa: F401
        ActiveSession,
        Base,
        Channel,
        ChannelFavorite,
        Config,
        MovieCatalog,
        MovieMetadata,
        MovieStream,
        Replay,
        ScraperFailure,
        SeriesCatalog,
        SeriesEpisode,
        SeriesMetadata,
        SeriesStream,
        SyncMetadata,
        User,
        WatchProgress,
    )

    tables = Base.metadata.tables.keys()
    expected = {
        "channels",
        "channel_favorites",
        "movies_catalog",
        "movie_streams",
        "movies_metadata",
        "series_catalog",
        "series_episodes",
        "series_streams",
        "series_metadata",
        "users",
        "active_sessions",
        "watch_progress",
        "replays",
        "scraper_failures",
        "config",
        "sync_metadata",
    }
    missing = expected - set(tables)
    assert not missing, f"Missing tables: {missing}"


def test_schemas_imports() -> None:
    from iptv_db.schemas import (  # noqa: F401
        ActiveSessionDB,
        ChannelDB,
        ChannelFavoriteDB,
        ConfigDB,
        MovieCatalogDB,
        MovieMetadataDB,
        MovieStreamDB,
        ReplayDB,
        ScraperFailureDB,
        SeriesCatalogDB,
        SeriesEpisodeDB,
        SeriesMetadataDB,
        SeriesStreamDB,
        SyncMetadataDB,
        UserDB,
        WatchProgressDB,
    )


def test_engine_factories() -> None:
    from iptv_db.engine import build_url

    url = build_url("localhost", 5432, "test", "user", "pass")
    assert url == "postgresql+psycopg://user:pass@localhost:5432/test"


def test_exceptions_hierarchy() -> None:
    from iptv_db.exceptions import (
        ConnectionError,
        ConstraintViolationError,
        DatabaseError,
        NotFoundError,
    )

    assert issubclass(NotFoundError, DatabaseError)
    assert issubclass(ConstraintViolationError, DatabaseError)
    assert issubclass(ConnectionError, DatabaseError)
