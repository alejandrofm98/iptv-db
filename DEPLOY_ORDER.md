# iptv-db Deploy Order

> Orden correcto de deploy cuando hay cambios en el schema. Si se hace en
> orden incorrecto, los consumers pueden fallar en runtime.

## Principios

1. **iptv-db primero** (source of truth del schema)
2. **Consumers despues** (iptv-api, scrapper), cuando sus hashes pineados apunten
   al nuevo commit de iptv-db

## Escenarios

### Escenario 1: Cambio solo en iptv-db (sin cambios en consumers)

```bash
# 1. Commit + push en iptv-db
cd iptv-db
git add alembic/versions/
git commit -m "feat: add new migration"
git push origin main

# 2. NO requiere re-deploy de consumers
#    (siempre que no haya cambios en modelos, solo en migrations)
```

### Escenario 2: Cambio en modelos de iptv-db (consumers necesitan update)

```bash
# 1. Commit + push en iptv-db
cd iptv-db
git add src/iptv_db/models/
git commit -m "feat: add new model"
git push origin main

# 2. Obtener el nuevo commit hash
NEW_HASH=$(git rev-parse HEAD)
echo "Nuevo hash: $NEW_HASH"

# 3. En iptv-api: actualizar requirements.txt
cd /home/alejandro/PycharmProjects/iptv-api
sed -i "s|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@[a-f0-9]*|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@$NEW_HASH|" requirements.txt
git add requirements.txt
git commit -m "chore: bump iptv-db to $NEW_HASH"
git push origin <branch>

# 4. En walactv-scrapper: actualizar requirements files (4 archivos)
cd /home/alejandro/PycharmProjects/walactv-scrapper
for f in docker/config/requirements*.txt; do
  sed -i "s|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@[a-f0-9]*|iptv-db @ git+https://github.com/alejandrofm98/iptv-db.git@$NEW_HASH|" "$f"
done
git add docker/config/
git commit -m "chore: bump iptv-db to $NEW_HASH"
git push origin master

# 5. Dokploy detecta los pushes y redespliega
#    Orden de deploy (automatico por Dokploy):
#    - iptv-api: redespliega con el nuevo hash de iptv-db
#    - scrapper: redespliega con el nuevo hash de iptv-db
#    - Los consumers usan pip install git+https://iptv-db.git@<nuevo_hash>
```

### Escenario 3: Cambio solo en consumers (no requiere cambio en iptv-db)

```bash
# 1. Commit + push en el consumer (iptv-api o scrapper)
#    (sin cambios en iptv-db)
cd /home/alejandro/PycharmProjects/iptv-api
git commit -m "feat: add new endpoint"
git push origin <branch>

# 2. NO requiere re-deploy de iptv-db
```

### Escenario 4: Cambio destructivo en iptv-db (requiere coordinacion)

```bash
# 1. Aplicar cambio en 2 fases (ver MIGRATION_GUIDE.md):
#    a. Migration 1: agregar nueva estructura (nullable, no destructiva)
#    b. Deploy consumers con hash nuevo (todavia toleran ambas estructuras)
#    c. Migration 2: eliminar estructura vieja
#    d. Deploy consumers con hash nuevo (ya no toleran estructura vieja)

# 2. Coordinar con el owner antes de proceder
```

## Orden de deploy automatizado (Dokploy)

Dokploy detecta pushes en cualquier branch configurada y redespliega automaticamente. El orden depende de cuando cada push llega:

| Push a | Dokploy detecta | Redeploy |
|--------|-----------------|----------|
| `iptv-db` (main) | NO tiene Dokploy (no es servicio deployable) | N/A |
| `iptv-api` (master) | SI | Redeploy de iptv-api |
| `iptv-api` (migracion-sqlalchemy-v2) | SI (si esta configurado) | Redeploy de iptv-api |
| `walactv-scrapper` (master) | SI | Redeploy de scrapper + sus 6 crons |

## Verificacion post-deploy

Despues de cada deploy, verificar que:

1. **Containers `Up`**: `docker ps --filter "name=walactv" --format "table {{.Names}}\t{{.Status}}"`
2. **Crons corren sin error**: `journalctl -u ofelia-scheduler --since "5 minutes ago"`
3. **Deploy log sin errores**: ver logs en `/etc/dokploy/logs/<app>/`
4. **Alertas del orquestador**: si el orquestador tiene acceso SSH, puede verificar automaticamente (ver AGENTS.md seccion "Verificacion de deploy post-push")

## Coordinacion con el orquestador

Si el orquestador (yo) tiene acceso SSH al server de Dokploy:
1. Push en cualquier repo
2. Decirle al orquestador "verifica el deploy de <app>"
3. El orquestador se conecta via SSH y lee los logs
4. Si hay errores, los analiza y propone un fix
5. Vos decis si aplicar el fix
6. El orquestador commitea y pushea solo si vos autorizas

NO dar acceso automatico sin autorizacion explicita.

## Tabla de coordinacion

| Accion | Quien | Cuando |
|--------|-------|--------|
| Push a iptv-db | Vos | Despues de `alembic revision --autogenerate` y revision del archivo generado |
| Push a iptv-api | Vos | Despues de bumpear el hash de iptv-db en requirements.txt |
| Push a scrapper | Vos | Despues de bumpear el hash de iptv-db en los 4 requirements files |
| Verificar deploy | Vos o el orquestador (con SSH) | Despues de cada push, esperar 1-2 minutos para que Dokploy procese |
| Auto-correccion | El orquestador (solo si vos lo pedis) | Cuando hay errores en los logs de deploy |
