# Auditoria de schema — F1 pre-migracion

## Fuente
- Dump BD productiva: `/tmp/columns_dump.txt` (240 lineas, 20 tablas, 2026-07-20)
- ORM iptv-api: `iptv-api/app/models/*.py` (9 archivos, 16 modelos)
- BD adicionales: `alembic_version` (Alembic internal), `calendario`, `channel_mappings`, `channel_variants` (solo en BD/scrapper)
- Schema files: `iptv-api/database/schema.sql` (408 lineas), `walactv-scrapper/database/schema.sql` (678 lineas)

## Resumen

| Tabla | En ORM | En BD | Drift |
|-------|--------|-------|-------|
| users | ✓ | ✓ | Ninguno |
| active_sessions | ✓ | ✓ | Ninguno |
| channels | ✓ | ✓ | BD tiene 5 columnas extra: stream_url, ultimo_chequeo, estado_stream, tiempo_respuesta_ms, last_sync_at |
| channel_favorites | ✓ | ✓ | Ninguno |
| movies_metadata | ✓ | ✓ | Ordinal gaps (pos 3, 20-22): columnas eliminadas en BD. Columnas iguales. |
| movies_catalog | ✓ | ✓ | BD tiene 4 columnas extra: not_found, retry_count, last_error, last_sync_at |
| movie_streams | ✓ | ✓ | BD tiene UNIQUE(movie_id, provider_id) no declarado en ORM |
| series_metadata | ✓ | ✓ | Ordinal gaps. Columnas iguales. |
| series_catalog | ✓ | ✓ | BD tiene 4 columnas extra: not_found, retry_count, last_error, last_sync_at. UNIQUE(tmdb_id) WHERE tmdb_id IS NOT NULL en BD no en ORM. |
| series_episodes | ✓ | ✓ | BD tiene 3 columnas extra: tmdb_not_found, tmdb_retry_count, tmdb_last_error |
| series_streams | ✓ | ✓ | BD tiene UNIQUE(episode_id, provider_id) no declarado en ORM |
| config | ✓ | ✓ | Ninguno |
| sync_metadata | ✓ | ✓ | Defaults differ (BD tiene defaults 0 para int cols) |
| replays | ✓ | ✓ | Ninguno |
| watch_progress | ✓ | ✓ | Ninguno |
| scraper_failures | ✓ | ✓ | BD tiene 2 UNIQUE indexes parciales no declarados en ORM: idx_failures_provider WHERE provider_id IS NOT NULL, idx_failures_series WHERE series_key IS NOT NULL |
| calendario | ✗ | ✓ | Solo scrapper. 11 columnas. UNIQUE(fecha, hora, equipos) |
| channel_mappings | ✗ | ✓ | Solo scrapper. 5 columnas. UNIQUE(source_name) |
| channel_variants | ✗ | ✓ | Solo scrapper. 6 columnas. FK a channels y channel_mappings |
| alembic_version | ✗ | ✓ | Tabla interna de Alembic |

## Tabla: users
- Columnas en BD: id (UUID PK), username (VARCHAR 50 UNIQUE NOT NULL), password_hash (VARCHAR 255 NOT NULL), max_connections (INT DEFAULT 2), is_active (BOOLEAN DEFAULT true), role (VARCHAR 20 DEFAULT 'user'), expires_at (TIMESTAMPTZ), created_at (TIMESTAMPTZ DEFAULT now()), updated_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: id, username, password_hash, max_connections, is_active, role, expires_at, created_at, updated_at
- Drift detectado: ninguno

## Tabla: active_sessions
- Columnas en BD: id (UUID PK), user_id (UUID FK NOT NULL), device_id (VARCHAR 64 NOT NULL), device_name (VARCHAR 100), device_type (VARCHAR 20 DEFAULT 'unknown'), ip_address (VARCHAR 45), user_agent (TEXT), last_activity (TIMESTAMPTZ DEFAULT now()), created_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: id, user_id, device_id, device_name, device_type, ip_address, user_agent, last_activity, created_at
- Drift detectado: ninguno

## Tabla: channels
- Columnas en BD: id (VARCHAR 50 PK), numero (INT), provider_id (VARCHAR 50), nombre (VARCHAR 255 NOT NULL), logo (TEXT), url (TEXT NOT NULL), grupo (VARCHAR 255), country (VARCHAR 10), tvg_id (VARCHAR 100), created_at (TIMESTAMPTZ DEFAULT now()), nombre_normalizado (VARCHAR 255), grupo_normalizado (VARCHAR 255), **stream_url (TEXT)**, **ultimo_chequeo (TIMESTAMPTZ)**, **estado_stream (TEXT)**, **tiempo_respuesta_ms (INT)**, **last_sync_at (TIMESTAMPTZ DEFAULT now())**
- Columnas en ORM: id, provider_id, nombre, nombre_normalizado, logo, grupo, grupo_normalizado, country, url, numero, tvg_id, created_at
- Drift detectado: BD tiene 5 columnas extra: `stream_url`, `ultimo_chequeo`, `estado_stream`, `tiempo_respuesta_ms`, `last_sync_at`
- Decision: **NO decidir en F1**, dejar nota para F1.5 con el owner

## Tabla: channel_favorites
- Columnas en BD: user_id (UUID PK, FK), channel_provider_id (VARCHAR 100 PK), created_at (TIMESTAMPTZ NOT NULL DEFAULT now())
- Columnas en ORM: user_id, channel_provider_id, created_at
- Drift detectado: ninguno

## Tabla: movies_metadata
- Columnas en BD: id (UUID PK), tmdb_id (VARCHAR 20 UNIQUE), title (VARCHAR 255), original_title (VARCHAR 255), overview_es (TEXT), overview_en (TEXT), genres (ARRAY), vote_average (FLOAT), vote_count (INT), poster_path (VARCHAR 255), backdrop_path (VARCHAR 255), release_date (DATE), year (INT), runtime_minutes (INT), tagline (VARCHAR 500), popularity (FLOAT), status (VARCHAR 50), imdb_id (VARCHAR), tmdb_data (JSONB), scraped_at (TIMESTAMPTZ DEFAULT now()), updated_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: id, tmdb_id, title, original_title, overview_es, overview_en, genres, vote_average, vote_count, poster_path, backdrop_path, release_date, year, runtime_minutes, tagline, popularity, status, imdb_id, tmdb_data, scraped_at, updated_at
- Drift detectado: ninguno (hay posiciones ordinales 3, 20-21-22 sin columna — columnas eliminadas en BD)

## Tabla: movies_catalog
- Columnas en BD: id (UUID PK), title (TEXT NOT NULL), provider_id (VARCHAR 50), tmdb_id (VARCHAR 20 FK), nombre_dedup_key (TEXT), year (INT), group_normalizado (TEXT), logo (TEXT), created_at (TIMESTAMPTZ), updated_at (TIMESTAMPTZ), **not_found (BOOLEAN DEFAULT false)**, **retry_count (INT DEFAULT 0)**, **last_error (TEXT)**, canonical_key (VARCHAR), **last_sync_at (TIMESTAMPTZ DEFAULT now())**, countries (ARRAY DEFAULT '{}')
- Columnas en ORM: id, title, provider_id, tmdb_id, nombre_dedup_key, canonical_key, year, countries, group_normalizado, logo, created_at, updated_at
- Drift detectado: BD tiene 4 columnas extra: `not_found`, `retry_count`, `last_error`, `last_sync_at`
- Indices extra en BD: uq_movies_catalog_tmdb UNIQUE(tmdb_id) WHERE tmdb_id IS NOT NULL, idx_movies_catalog_scrape, idx_movies_catalog_dedup, idx_movies_catalog_canonical, idx_movies_catalog_countries GIN, idx_movies_catalog_group, idx_movies_catalog_tmdb, idx_movies_catalog_year
- Decision: **NO decidir en F1**, dejar nota para F1.5 con el owner

## Tabla: movie_streams
- Columnas en BD: id (UUID PK), movie_id (UUID FK NOT NULL), country (VARCHAR 10 NOT NULL), quality (VARCHAR 10), provider_id (VARCHAR 50), stream_url (TEXT NOT NULL), url (TEXT), label (TEXT), numero (INT DEFAULT 0), created_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: id, movie_id, country, quality, provider_id, stream_url, url, label, numero, created_at
- Drift detectado: ninguno en columnas
- UNIQUE(movie_id, provider_id) en BD no declarado en ORM

## Tabla: series_metadata
- Columnas en BD: id (UUID PK), tmdb_id (VARCHAR 20 UNIQUE), title (VARCHAR 255), original_title (VARCHAR 255), overview_es (TEXT), overview_en (TEXT), genres (ARRAY), vote_average (FLOAT), vote_count (INT), poster_path (VARCHAR 255), backdrop_path (VARCHAR 255), release_date (DATE), year (INT), tagline (VARCHAR 500), popularity (FLOAT), status (VARCHAR 50), tmdb_data (JSONB), scraped_at (TIMESTAMPTZ DEFAULT now()), updated_at (TIMESTAMPTZ DEFAULT now()), imdb_id (VARCHAR)
- Columnas en ORM: id, tmdb_id, title, original_title, overview_es, overview_en, genres, vote_average, vote_count, poster_path, backdrop_path, release_date, year, tagline, popularity, status, imdb_id, tmdb_data, scraped_at, updated_at
- Drift detectado: ninguno

## Tabla: series_catalog
- Columnas en BD: id (UUID PK), title (TEXT NOT NULL), series_key (TEXT NOT NULL), provider_id (VARCHAR 50), tmdb_id (VARCHAR 20 FK), nombre_dedup_key (TEXT), year (INT), group_normalizado (TEXT), logo (TEXT), created_at (TIMESTAMPTZ), updated_at (TIMESTAMPTZ), **not_found (BOOLEAN DEFAULT false)**, **retry_count (INT DEFAULT 0)**, **last_error (TEXT)**, canonical_key (VARCHAR), **last_sync_at (TIMESTAMPTZ DEFAULT now())**, countries (ARRAY DEFAULT '{}')
- Columnas en ORM: id, title, series_key, canonical_key, provider_id, tmdb_id, nombre_dedup_key, year, countries, group_normalizado, logo, created_at, updated_at
- Drift detectado: BD tiene 4 columnas extra: `not_found`, `retry_count`, `last_error`, `last_sync_at`
- Indices extra en BD: uq_series_catalog_tmdb UNIQUE(tmdb_id) WHERE tmdb_id IS NOT NULL, idx_series_catalog_scrape, idx_series_catalog_series_key, idx_series_catalog_canonical, idx_series_catalog_countries GIN, idx_series_catalog_group, idx_series_catalog_tmdb, idx_series_catalog_year
- Decision: **NO decidir en F1**, dejar nota para F1.5 con el owner

## Tabla: series_episodes
- Columnas en BD: id (UUID PK), catalog_id (UUID FK NOT NULL), season_number (INT NOT NULL), episode_number (INT NOT NULL), title (TEXT), overview (TEXT), air_date (DATE), still_path (VARCHAR 255), numero (INT), title_en (TEXT), overview_en (TEXT), runtime (INT), vote_average (NUMERIC), vote_count (INT), episode_type (VARCHAR 50), tmdb_checked (BOOLEAN DEFAULT false), **tmdb_not_found (BOOLEAN DEFAULT false)**, **tmdb_retry_count (INT DEFAULT 0)**, **tmdb_last_error (TEXT)**
- Columnas en ORM: id, catalog_id, season_number, episode_number, title, overview, air_date, still_path, numero, title_en, overview_en, runtime, vote_average, vote_count, episode_type, tmdb_checked
- Drift detectado: BD tiene 3 columnas extra: `tmdb_not_found`, `tmdb_retry_count`, `tmdb_last_error`
- Decision: **NO decidir en F1**, dejar nota para F1.5 con el owner

## Tabla: series_streams
- Columnas en BD: id (UUID PK), episode_id (UUID FK NOT NULL), country (VARCHAR 10 NOT NULL), quality (VARCHAR 10), provider_id (VARCHAR 50), stream_url (TEXT NOT NULL), url (TEXT), label (TEXT), numero (INT DEFAULT 0), created_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: id, episode_id, country, quality, provider_id, stream_url, url, label, numero, created_at
- Drift detectado: ninguno en columnas
- UNIQUE(episode_id, provider_id) en BD no declarado en ORM

## Tabla: config
- Columnas en BD: key (TEXT PK), value (TEXT), description (TEXT), updated_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: key, value, description, updated_at
- Drift detectado: ninguno

## Tabla: sync_metadata
- Columnas en BD: id (VARCHAR 50 PK), ultima_actualizacion (TIMESTAMPTZ), total_canales (INT DEFAULT 0), total_movies (INT DEFAULT 0), total_series (INT DEFAULT 0), m3u_template_path (TEXT), m3u_template_filename (TEXT), m3u_size_mb (NUMERIC), channels_con_logo (INT DEFAULT 0), channels_sin_logo (INT DEFAULT 0), movies_con_logo (INT DEFAULT 0), movies_sin_logo (INT DEFAULT 0), series_con_logo (INT DEFAULT 0), series_sin_logo (INT DEFAULT 0), created_at (TIMESTAMPTZ DEFAULT now()), updated_at (TIMESTAMPTZ DEFAULT now()), channels_generated_at (TIMESTAMPTZ), channels_json_size_mb (NUMERIC), movies_generated_at (TIMESTAMPTZ), movies_json_size_mb (NUMERIC), series_generated_at (TIMESTAMPTZ), series_json_size_mb (NUMERIC)
- Columnas en ORM: id, ultima_actualizacion, total_canales, total_movies, total_series, m3u_template_path, m3u_template_filename, m3u_size_mb, channels_con_logo, channels_sin_logo, movies_con_logo, movies_sin_logo, series_con_logo, series_sin_logo, created_at, updated_at, channels_generated_at, channels_json_size_mb, movies_generated_at, movies_json_size_mb, series_generated_at, series_json_size_mb
- Drift detectado: ninguno (defaults 0 en BD no declarados en ORM, menor)

## Tabla: scraper_failures
- Columnas en BD: id (UUID PK), provider_id (VARCHAR 50), series_key (VARCHAR 255), title (TEXT NOT NULL), year (INT), error_message (TEXT), failed_at (TIMESTAMPTZ DEFAULT now()), retry_count (INT DEFAULT 1), last_retry_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: id, provider_id, series_key, title, year, error_message, failed_at, retry_count, last_retry_at
- Indices extra en BD: idx_failures_provider UNIQUE(provider_id) WHERE provider_id IS NOT NULL, idx_failures_series UNIQUE(series_key) WHERE series_key IS NOT NULL
- Drift detectado: ninguno en columnas. Indices parciales UNIQUE en BD no declarados en ORM.

## Tabla: watch_progress
- Columnas en BD: id (UUID PK), user_id (UUID FK NOT NULL), content_id (VARCHAR 100 NOT NULL), content_type (VARCHAR 20 NOT NULL), position_ms (BIGINT NOT NULL DEFAULT 0), duration_ms (BIGINT NOT NULL DEFAULT 0), series_name (VARCHAR 255), season_number (INT), episode_number (INT), title (VARCHAR 255 NOT NULL DEFAULT ''), image_url (TEXT NOT NULL DEFAULT ''), last_watched_at (TIMESTAMPTZ DEFAULT now()), is_watched (BOOLEAN DEFAULT false)
- Columnas en ORM: id, user_id, content_id, content_type, position_ms, duration_ms, series_name, season_number, episode_number, title, image_url, last_watched_at, is_watched
- Drift detectado: ninguno

## Tabla: replays
- Columnas en BD: id (UUID PK), slug (TEXT UNIQUE NOT NULL), source_site (TEXT NOT NULL), title (TEXT NOT NULL), event_name (TEXT), event_type (TEXT), event_date (DATE), post_url (TEXT NOT NULL), featured_image_url (TEXT), description (TEXT), video_sources (JSONB NOT NULL), match_card (JSONB NOT NULL), created_at (TIMESTAMPTZ DEFAULT now()), updated_at (TIMESTAMPTZ DEFAULT now())
- Columnas en ORM: id, slug, source_site, title, event_name, event_type, event_date, post_url, featured_image_url, description, video_sources, match_card, created_at, updated_at
- Drift detectado: ninguno

## Tablas solo en BD (scrapper, no ORM)

### calendario
- 11 columnas: id (UUID PK), fecha (DATE NOT NULL), hora (TEXT NOT NULL), competicion (TEXT), categoria (TEXT), equipos (TEXT NOT NULL), canales (ARRAY), created_at (TIMESTAMPTZ), updated_at (TIMESTAMPTZ), imagen_evento (TEXT), subtitulo_competicion (TEXT)
- UNIQUE(fecha, hora, equipos)
- Indices: idx_calendario_categoria, idx_calendario_fecha, idx_calendario_equipos (GIN tsvector)

### channel_mappings
- 5 columnas: id (BIGSERIAL PK), source_name (TEXT UNIQUE NOT NULL), display_name (TEXT NOT NULL), created_at (TIMESTAMPTZ), updated_at (TIMESTAMPTZ)
- Indices: idx_mappings_display, idx_mappings_source

### channel_variants
- 6 columnas: id (BIGSERIAL PK), mapping_id (BIGINT FK NOT NULL), channel_id (VARCHAR 50 FK), quality (TEXT DEFAULT 'HD'), priority (INT DEFAULT 0), created_at (TIMESTAMPTZ)
- FK: channel_variants_mapping_id_fkey → channel_mappings(id), channel_variants_channel_id_fkey → channels(id)
- Indices: idx_variants_channel, idx_variants_mapping, idx_variants_priority

## Decisiones pendientes
- [ ] Columnas legacy en BD sin ORM (channels: stream_url, ultimo_chequeo, estado_stream, tiempo_respuesta_ms, last_sync_at; movies_catalog/series_catalog: not_found, retry_count, last_error, last_sync_at; series_episodes: tmdb_not_found, tmdb_retry_count, tmdb_last_error)
- [ ] Columnas en ORM sin BD: ninguna
- [ ] Indices/FKs faltantes en ORM: UNIQUE(movie_id, provider_id) en movie_streams, UNIQUE(episode_id, provider_id) en series_streams, UNIQUE partials en scraper_failures, UNIQUE partials en movies_catalog/series_catalog
- [ ] Tablas del scrapper no modeladas en ORM: calendario, channel_mappings, channel_variants — ¿crear modelos en iptv-db para F1.5?
- [ ] Defaults de sync_metadata (BD tiene DEFAULT 0, ORM no tiene defaults)
- [ ] watch_progress UNIQUE usa NULLS NOT DISTINCT en BD para manejar NULL en season_number/episode_number
