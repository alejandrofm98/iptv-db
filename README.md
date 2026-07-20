# iptv-db

Shared database layer for iptv-api and walactv-scrapper.

## Install (editable, dev)

```bash
cd /home/alejandro/PycharmProjects/iptv-db
pip install -e ".[dev]"
```

## Install (from git)

```bash
pip install git+https://github.com/alejandrofm98/iptv-db.git@v0.1.0
```

## Usage

```python
from iptv_db.engine import get_sync_engine, get_sync_session_factory, session_scope
from iptv_db.models import MovieCatalog

engine = get_sync_engine("postgresql+psycopg://user:pass@host:5432/db")
Session = get_sync_session_factory(engine)

with session_scope(Session) as session:
    movies = session.query(MovieCatalog).filter_by(title="Inception").all()
```

## Migrations

```bash
alembic upgrade head
alembic revision --autogenerate -m "add column"
```

## Layout

- `models/` — SQLAlchemy 2.0 ORM (herencia concrete para Movie/Series)
- `schemas/` — Pydantic DB DTOs (1:1 con tablas)
- `engine.py` — engine y session factories (sync + async)
- `exceptions.py` — jerarquia de errores de BD
- `migrations/` — Alembic

## Status

F1 — modelos consolidados, sin cambios de schema. Migraciones se haran en F1.5 tras auditoria documentada en MIGRATION_NOTES.md.
