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
        PlaybackPreference,
        Replay,
        ScraperFailure,
        SeriesCatalog,
        SeriesEpisode,
        SeriesMetadata,
        SeriesStream,
        SyncMetadata,
        User,
        VideoSegment,
        VideoSegmentSync,
        VodFavorite,
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
        "playback_preferences",
        "replays",
        "scraper_failures",
        "video_segment_sync",
        "video_segments",
        "vod_favorites",
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
        VodFavoriteDB,
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


def test_video_segment_constraints() -> None:
    from iptv_db.models import Base, VideoSegment, VideoSegmentSync

    segments = Base.metadata.tables[VideoSegment.__tablename__]
    sync = Base.metadata.tables[VideoSegmentSync.__tablename__]

    assert [column.name for column in segments.primary_key.columns] == ["id"]
    assert {column.name for column in sync.primary_key.columns} == {"episode_id", "source"}
    assert any(
        list(constraint.columns.keys()) == ["episode_id", "segment_type", "source"]
        for constraint in segments.constraints
        if constraint.__class__.__name__ == "UniqueConstraint"
    )
    check_sql = {
        str(constraint.sqltext)
        for constraint in segments.constraints
        if constraint.__class__.__name__ == "CheckConstraint"
    }
    assert "segment_type IN ('intro', 'recap', 'outro')" in check_sql
    assert "start_ms >= 0" in check_sql
    assert "end_ms > start_ms" in check_sql
