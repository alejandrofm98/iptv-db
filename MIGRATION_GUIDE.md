# iptv-db Migration Guide

## Overview

Single source of truth for the IPTV database schema across the entire ecosystem:
`iptv-api`, `walactv-scrapper`, and any future clients.

All migrations live in `src/iptv_db/migrations/versions/`, generated from the ORM
models in `src/iptv_db/models/`.

## Workflow

### Create a new migration

```bash
cd iptv-db

# 1. Edit ORM models in src/iptv_db/models/
# 2. Autogenerate the migration
alembic revision --autogenerate -m "description_of_change"

# 3. Review the generated file in alembic/versions/
# 4. Test locally (requires local Postgres)
alembic upgrade head
alembic downgrade -1  # verify rollback works

# 5. Verify idempotence (against a local DB with the schema already applied)
alembic check  # should say "No new upgrade operations detected"
```

### Apply migrations to production

```bash
cd iptv-db
DATABASE_URL="postgresql+psycopg://user:pass@host:5432/dbname" alembic upgrade head
```

Or via env vars (used by `env.py`):

```bash
PG_HOST=your_host PG_PORT=5432 PG_DATABASE=iptv \
  PG_USER=your_user PG_PASSWORD=your_pass \
  alembic upgrade head
```

### Rollback

```bash
alembic downgrade -1      # one step back
alembic downgrade <rev>   # to a specific revision
```

## Repository structure

```
iptv-db/
├── src/iptv_db/
│   ├── models/                 # SQLAlchemy 2.0 ORM (autogenerate source)
│   │   ├── __init__.py         # exports all models
│   │   ├── base.py             # DeclarativeBase + mixins
│   │   ├── calendario.py       # sports calendar (scrapper)
│   │   ├── channel.py          # channels + channel_favorites
│   │   ├── channel_mapping.py  # source→display name map (scrapper)
│   │   ├── channel_variant.py  # quality/priority variants (scrapper)
│   │   ├── config.py           # config + sync_metadata
│   │   ├── content.py          # movies_metadata, movies_catalog, movie_streams
│   │   ├── replay.py           # event replays
│   │   ├── scraper.py          # scraper_failures
│   │   ├── series.py           # series_metadata, series_catalog, episodes, streams
│   │   ├── user.py             # users + active_sessions
│   │   └── watch_progress.py   # watch_progress
│   ├── migrations/
│   │   ├── env.py              # Alembic environment (async, reads PG_* env vars)
│   │   ├── script.py.mako      # migration template
│   │   └── versions/           # migration scripts (history)
│   ├── engine/                 # SQLAlchemy engine factories
│   ├── exceptions/             # DB exception hierarchy
│   └── schemas/                # Pydantic DTOs
├── alembic.ini                 # Alembic configuration
├── MIGRATION_NOTES.md          # Drift analysis (historical reference)
├── MIGRATION_GUIDE.md          # This file
└── pyproject.toml              # Project configuration
```

## Files superseded

These files still exist in sibling repositories but are **no longer the source of truth**:

| File | Location | Status |
|------|----------|--------|
| `alembic/versions/b6608c246678_...` | iptv-api | Legacy (kept as reference) |
| `alembic/versions/50987149425c_...` | iptv-api | Legacy (kept as reference) |
| `alembic/versions/309bd59b0f90_...` | iptv-api | Legacy (kept as reference) |
| `database/schema.sql` | iptv-api | Superseded |
| `database/schema.sql.legacy` | walactv-scrapper | Renamed (not source of truth) |
| `database/insert.sql.legacy` | walactv-scrapper | Renamed (not source of truth) |

## Important notes

1. **Always use `alembic check` before deploying** to catch drift between ORM and DB.
2. **Migration idempotence**: after applying all migrations, `alembic check` should
   report "No new upgrade operations detected".
3. **The 3 legacy migrations** in `iptv-api/alembic/versions/` are kept as historical
   reference only. They can be deleted after the unified migration has been applied
   to production and verified.
4. **The `.legacy` files** in `walactv-scrapper/database/` can be deleted after the
   unified migration has been verified in production.
