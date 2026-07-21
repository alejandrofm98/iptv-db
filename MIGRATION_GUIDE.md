# iptv-db Migration Guide

> Como crear, aplicar y rollback de migrations Alembic en iptv-db.

## Setup inicial (solo la primera vez)

```bash
cd iptv-db
pip install -e ".[dev]"
```

## Crear una nueva migration

### Workflow basico

```bash
# 1. Editar el modelo en src/iptv_db/models/<file>.py
#    Ej: agregar columna `new_field: Mapped[str | None] = mapped_column(String(100), nullable=True)`

# 2. Generar la migration con autogenerate
alembic revision --autogenerate -m "add new_field to channels"

# 3. Revisar el archivo generado en alembic/versions/
#    VERIFICAR:
#    - Solo CREATE TABLE / CREATE INDEX (no DROP)
#    - La columna se llama correcto
#    - El tipo es correcto (String(100), no Text)
#    - Los constraints (UNIQUE, FK) estan presentes

# 4. Test local (BD de prueba)
createdb iptv_test
DATABASE_URL="postgresql+psycopg://user:pass@localhost:5432/iptv_test" alembic upgrade head
DATABASE_URL="..." alembic downgrade -1  # verificar rollback
DATABASE_URL="..." alembic upgrade head  # re-aplicar

# 5. Commit + push
git add alembic/versions/
git commit -m "feat(models): add new_field to channels"
git push origin main

# 6. Notificar a consumers (iptv-api, scrapper) para que bumpen el hash
```

### Cuando autogenerate falla

A veces autogenerate no detecta cambios (ej: cambios de server_default, CHECK constraints). En ese caso:

```bash
# Crear migration vacia
alembic revision -m "add manual change to X"

# Editar el archivo generado y agregar manualmente:
def upgrade() -> None:
    op.execute("ALTER TABLE X ADD CONSTRAINT ...")
def downgrade() -> None:
    op.execute("ALTER TABLE X DROP CONSTRAINT ...")
```

### Casos especiales

#### Agregar columna NOT NULL a tabla con datos existentes

```python
def upgrade() -> None:
    # 1. Agregar como nullable
    op.add_column('channels', sa.Column('new_field', sa.String(100), nullable=True))

    # 2. Poblar con valor por defecto
    op.execute("UPDATE channels SET new_field = 'default_value' WHERE new_field IS NULL")

    # 3. Alterar a NOT NULL
    op.alter_column('channels', 'new_field', nullable=False)
```

#### Renombrar columna o tabla

```python
def upgrade() -> None:
    op.alter_column('old_name', 'new_name', new_column_name='new_name')
    # o
    op.rename_table('old_table', 'new_table')
```

#### Cambiar tipo de columna

```python
def upgrade() -> None:
    # Postgres-specific: puede requerir USING
    op.alter_column(
        'channels',
        'id',
        type_=sa.BigInteger(),
        postgresql_using='id::bigint'
    )
```

## Aplicar migrations

### En una BD nueva (fresh)

```bash
DATABASE_URL="postgresql+psycopg://user:pass@host:5432/db" alembic upgrade head
```

### En una BD existente (con datos)

```bash
# 1. Backup primero
pg_dump -h host -U user -d db -F c -f /tmp/backup.dump

# 2. Dry-run (ver SQL sin ejecutar)
DATABASE_URL="..." alembic upgrade head --sql

# 3. Aplicar
DATABASE_URL="..." alembic upgrade head
```

### Marcar como aplicada sin ejecutar (squash)

Si las tablas ya existen (ej: setup manual) y queres marcar la migration como aplicada:

```bash
# Solo cuando sabes lo que haces
alembic stamp head
```

## Rollback

```bash
# Rollback una migration
alembic downgrade -1

# Rollback a una version especifica
alembic downgrade <revision>

# Rollback completo
alembic downgrade base
```

## Verificar estado

```bash
# Ver migration actual
alembic current

# Ver historial
alembic history

# Ver diff entre modelo y BD
alembic check
```

## Troubleshooting

### "Can't locate revision X"

La BD tiene una version que no existe en la carpeta `alembic/versions/`. Soluciones:
1. Verificar que clonaste el repo correcto
2. Si el problema es chain legacy (ej: iptv-api antiguo), usar `alembic stamp <nueva_revision>` para squashear

### "Target database is not up to date"

Hay migrations sin aplicar. Ejecutar `alembic upgrade head`.

### "Multiple head revisions are present"

Hay branches de migration divergentes. Necesitas una migration de merge:

```bash
alembic merge -m "merge branches" <rev1> <rev2>
```

## Comandos utiles

| Comando | Descripcion |
|---------|-------------|
| `alembic current` | Ver la version actual de la BD |
| `alembic history --verbose` | Ver historial detallado de migrations |
| `alembic heads` | Ver las heads de branches de migration |
| `alembic branches` | Ver branches activos |
| `alembic show <rev>` | Ver el contenido de una migration |
| `alembic upgrade +1` | Aplicar la siguiente migration |
| `alembic downgrade -1` | Rollback la ultima migration |

## Versionado y deploy

- Las migrations son backward-compatible (CREATE TABLE, ADD COLUMN nullable, CREATE INDEX)
- Evitar cambios destructivos en una migration aplicada a prod
- Si necesitas un cambio destructivo, hacerlo en 2 migrations:
  1. Primera: agregar la nueva estructura (nullable, etc.)
  2. Deploy
  3. Segunda: eliminar la estructura vieja
  4. Deploy

## Coordinacion con consumers

- iptv-api y scrapper pinean un commit hash especifico de iptv-db en sus requirements
- Cuando cambias el schema en iptv-db:
  1. Commit + push en iptv-db
  2. Notificar a consumers para que bumpen el hash
  3. Consumers hacen su propio deploy
- Ver `DEPLOY_ORDER.md` para el orden de deploy
