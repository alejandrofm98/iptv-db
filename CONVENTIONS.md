# iptv-db Coding Conventions

> Convenciones para contribuir a iptv-db. Cualquier PR que no las siga
> sera rechazado en el gate review (Oracle).

## Estilo de codigo

### Python
- Target: Python 3.12+
- Line length: 100
- Type hints: obligatorios en funciones publicas
- Docstrings: en ingles, formato Google
- Imports: stdlib -> terceros -> locales (ordenados con isort)
- Naming:
  - Clases: `PascalCase`
  - Funciones/variables: `snake_case`
  - Constantes: `UPPER_SNAKE_CASE`
  - Modelos SQLAlchemy: `PascalCase` singular (`Channel`, no `Channels`)

### SQLAlchemy
- Type hints con `Mapped[T]` (no `Column[T]`)
- Herencia: concrete para modelos polimorficos (ver `MetadataBase`, `CatalogBase`, `StreamBase`)
- Tablas: `__tablename__` en `snake_case` plural (`channels`, no `channel`)
- Constraints: `UniqueConstraint`, `Index` en `__table_args__`
- Foreign keys: usar `ondelete` explicito (`CASCADE`, `SET NULL`)
- Defaults: `server_default=...` para defaults a nivel SQL

### Commits
- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Scope opcional: `feat(models):`, `fix(engine):`
- Mensaje en imperativo ("add", no "added")

## Lint y formato

```bash
# Formateo
ruff format src/ tests/

# Lint (debe pasar sin warnings)
ruff check src/ tests/

# Tipos (strict mode en iptv-db)
mypy src/iptv_db

# Tests
pytest tests/ -v --cov=. --cov-report=term-missing
```

Configuracion en `pyproject.toml`. No commits si lint falla.

## Estructura de archivos

- `src/iptv_db/models/` — un archivo por dominio (user.py, channel.py, content.py, etc.)
- `src/iptv_db/schemas/` — un archivo por dominio, mismo nombre que el modelo
- `src/iptv_db/migrations/versions/` — archivos `.py` con nombre `{revision}_{descripcion}.py`
- `tests/` — un archivo por modulo (`test_models.py`, `test_engine.py`, etc.)

## Reglas de cambios

1. **NUNCA** hacer cambios destructivos en migraciones sin consultation:
   - `DROP COLUMN`: requiere aprobacion explicita del owner
   - `DROP TABLE`: requiere confirmacion de que no hay consumers
   - `ALTER COLUMN ... TYPE ... USING`: requiere backup previo

2. **Toda columna nueva** debe ser:
   - `nullable=True` O tener `server_default` (nunca `NOT NULL` sin default en tabla con datos)
   - Documentada en el docstring del modelo

3. **Tests pasan antes de commit**:
   - Tests unitarios para modelos nuevos
   - Tests de constraints (UNIQUE, FK, CHECK)
   - Test de idempotencia de la migracion (`alembic upgrade head` 2 veces = mismo resultado)

4. **Lint limpio**:
   - `ruff check` sin warnings
   - `mypy` strict mode sin errores
   - Format con `ruff format`

5. **Migrations siempre con autogenerate**:
   ```bash
   alembic revision --autogenerate -m "descripcion concisa"
   ```
   Revisar el archivo generado ANTES de commit. Alembic a veces se equivoca.

## Versionado del paquete

- Version en `pyproject.toml` segun SemVer
- Cambios breaking (cambios en modelos, signature de funciones publicas): bump MAJOR
- Nuevas features (nuevos modelos, helpers): bump MINOR
- Bugfixes: bump PATCH

Cuando bumpees version, actualizar:
- `pyproject.toml`: `version = "X.Y.Z"`
- Tag de git: `git tag vX.Y.Z`
- Notificar a consumers (iptv-api, walactv-scrapper) para que bumpen el hash pinneado
