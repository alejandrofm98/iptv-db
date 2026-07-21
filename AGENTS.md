# AGENTS.md - IPTV-DB

> Paquete compartido de ORM, DTOs, engine factories, excepciones y migraciones Alembic.
> Consumido por `iptv-api` y `walactv-scrapper`. Este NO es un servicio deployable.

## 0. Posicion en el ecosistema

```
   +-------------+
   |  iptv-api   |----usa----+
   +-------------+          |
                             v
                       +---------+
                       | iptv-db | <----usa----+------------+
                       | (este)  |              | walactv-   |
                       +---------+              | scrapper   |
                                                 +------------+
```

| Proyecto         | Como lo usa                                          |
|------------------|------------------------------------------------------|
| `iptv-api`       | Modelos via shims en `app/models/`, env.py apunta aca |
| `walactv-scrapper` | Modelos y engine en scripts, database.py gestiona ambos |
| `walactvWeb` / `WalacTV` | No lo usan directamente (consumen iptv-api) |

## 1. Contexto rapido

- **Stack**: Python 3.12, SQLAlchemy 2.0, Alembic, Pydantic 2.12, psycopg3
- **Source of truth**: este paquete es LA UNICA fuente de verdad para el schema de BD
- **Instalacion**: `pip install git+https://github.com/alejandrofm98/iptv-db.git@<commit_hash>`
- **Branch**: `main`
- **Tag pinning**: cada build de iptv-api y scrapper pinea un commit especifico (no branch, no tag)

## 2. Arquitectura

```
src/iptv_db/
├── models/           # 19 modelos ORM (SQLAlchemy 2.0)
│   ├── base.py       # Base, UUIDPKMixin, TimestampMixin
│   ├── user.py       # User, ActiveSession
│   ├── channel.py    # Channel, ChannelFavorite
│   ├── content.py    # MovieCatalog, MovieStream, MovieMetadata (+ CatalogBase, StreamBase abstractas)
│   ├── series.py     # SeriesCatalog, SeriesEpisode, SeriesStream, SeriesMetadata
│   ├── watch_progress.py
│   ├── replay.py
│   ├── scraper.py    # ScraperFailure
│   ├── config.py     # Config, SyncMetadata
│   ├── calendario.py # Calendario (tabla del scrapper)
│   ├── channel_mapping.py
│   └── channel_variant.py
├── schemas/          # 15 DTOs Pydantic 1:1 con tablas
├── engine.py         # get_sync_engine, get_async_engine, session_scope, build_url
├── exceptions.py     # DatabaseError, NotFoundError, ConstraintViolationError, ConnectionError
├── migrations/       # Alembic
│   ├── env.py
│   └── versions/     # 71fffd6203e2_initial_schema_unified.py (UNICA migration)
└── __init__.py
```

## 3. Patrones de uso

### 3.1 Importar modelos

```python
from iptv_db.models import (
    User, Channel, MovieCatalog, SeriesCatalog,
    MovieStream, SeriesEpisode, SeriesStream,
    ScraperFailure, Replay,
)

# Uso con SQLAlchemy 2.0
from iptv_db.models import Channel
session.query(Channel).filter_by(provider_id="123").first()
```

### 3.2 Engine factories

```python
from iptv_db.engine import (
    get_sync_engine, get_async_engine,
    get_sync_session_factory, get_async_session_factory,
    build_url, session_scope, async_session_scope,
)

# Sync (scripts one-shot, CLI, batch)
url = build_url(host="...", port=5432, database="...", user="...", password="...")
factory = get_sync_session_factory(url)
with session_scope(factory) as session:
    session.query(User).all()

# Async (FastAPI, scripts async)
factory = get_async_session_factory(url)
async with session_scope(factory) as session:
    result = await session.execute(select(Channel))
```

### 3.3 Excepciones

```python
from iptv_db.exceptions import (
    DatabaseError, NotFoundError, ConstraintViolationError, ConnectionError,
)

try:
    session.add(user)
except ConstraintViolationError:
    # unique violation, FK violation, etc.
    ...
except NotFoundError:
    # entity not found
    ...
```

## 4. Workflow de cambios

### 4.1 Agregar una columna

1. Editar `src/iptv_db/models/<file>.py` — agregar columna al modelo
2. `cd iptv-db && alembic revision --autogenerate -m "add column X"`
3. Revisar el archivo generado en `alembic/versions/`
4. `alembic upgrade head` (test local)
5. `alembic downgrade -1` (verificar rollback)
6. Commit + push a GitHub
7. Copiar el commit hash
8. Actualizar el hash en iptv-api/requirements.txt y scrapper/docker/config/requirements*.txt
9. Commit + push en esos repos
10. Dokploy redesplega

### 4.2 Agregar una tabla

Mismo flujo que columna. El modelo va en `src/iptv_db/models/<file>.py`.

### 4.3 Cambiar tipo de columna

1. Editar el modelo
2. `alembic revision --autogenerate` (detecta el cambio)
3. **CRITICO**: revisar el .py generado. Alembic puede generar `ALTER COLUMN ... TYPE ... USING ...` o un drop+create. Validar manualmente.
4. Test local + rollback
5. Push + bump hash en consumers

### 4.4 Versionado del hash

iptv-api y scrapper pinean un commit hash especifico en requirements. Cuando cambies iptv-db:

```bash
# En iptv-api
cd /home/alejandro/PycharmProjects/iptv-api
# requirements.txt linea 19
sed -i 's|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@OLD|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@NEW|g' requirements.txt
git add requirements.txt
git commit -m "chore: bump iptv-db to NEW"

# En walactv-scrapper
cd /home/alejandro/PycharmProjects/walactv-scrapper
for f in docker/config/requirements*.txt; do
  sed -i 's|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@OLD|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@NEW|g' "$f"
done
git add docker/config/
git commit -m "chore: bump iptv-db to NEW"
```

## 5. Configuracion

- **Variables de entorno para `build_url`**: `PG_HOST`, `PG_PORT`, `PG_DATABASE`, `PG_USER`, `PG_PASSWORD`
- **Driver**: `psycopg3` (no psycopg2 ni asyncpg)
- **Dialect SQLAlchemy**: `postgresql+psycopg` (sync) o `postgresql+psycopg` (async — psycopg3 soporta async nativo)

## 6. Lint, formato, tipos y calidad

Toda la config en `pyproject.toml`.

```bash
ruff format src/ tests/
ruff check src/ tests/ --fix
mypy src/iptv_db      # strict = true
pytest tests/
```

## 7. Testing

- Tests en `tests/test_imports.py`: verifican que todos los modelos se importan sin error
- Tests futuros: agregar tests de constraints, UNIQUE, defaults, JSONB serialization

## 8. Despliegue

**Este paquete NO se deploya.** Es un paquete Python que se instala via pip en iptv-api y walactv-scrapper.

- **No tiene Dokploy**
- **No tiene Dockerfile**
- **No tiene docker-compose**
- **No se pushea como servicio**

Cada vez que cambias algo aca, los consumers (iptv-api, scrapper) tienen que bumpear el hash.

## 9. Criterios para cambios

1. **Nunca hacer cambios destructivos** en migraciones sin consultation: `DROP COLUMN`, `DROP TABLE`, `ALTER COLUMN ... TYPE` con USING pueden perder data.
2. **Toda columna agregada debe ser nullable o tener DEFAULT**: nunca `NOT NULL` sin default en una tabla con datos existentes.
3. **Tests pasan antes de commit**: `pytest tests/`.
4. **Lint limpio**: `ruff check` sin warnings.
5. **Tipos OK**: `mypy` sin errores (strict mode).

## 10. Roadmap (no en esta iteracion)

1. ~~Crear paquete iptv-db~~ (F1, hecho)
2. ~~Migrar iptv-api y scrapper a iptv-db~~ (F2-F3, hecho)
3. ~~Generar migration inicial unificada~~ (F1.5, hecho)
4. Publicar iptv-db en PyPI para que `pip install iptv-db` funcione sin git URL
5. Crear tests de constraints y JSONB
6. Agregar type stubs (.pyi) para mejor IDE support en consumers

## 11. Checklist antes de cerrar una tarea

1. Tests pasan: `pytest tests/`
2. Lint limpio: `ruff check`
3. Tipos: `mypy` sin errores
4. Migracion validada: `alembic upgrade head` + `alembic downgrade -1` funcionan
5. Hash actualizado en iptv-api y scrapper (si la migracion rompe consumers)
6. Commit message describe el cambio de schema
7. Push a GitHub
