"""Add direct imdb_id to catalogs for Stremio addons without metadata join."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "f3a1c9e2b4d5"
down_revision: str | Sequence[str] | None = "7f3a9c1e4b2d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add imdb_id columns, indexes and backfill from existing metadata."""
    op.add_column("movies_catalog", sa.Column("imdb_id", sa.String(20), nullable=True))
    op.add_column("series_catalog", sa.Column("imdb_id", sa.String(20), nullable=True))
    op.create_index("ix_movies_catalog_imdb_id", "movies_catalog", ["imdb_id"])
    op.create_index("ix_series_catalog_imdb_id", "series_catalog", ["imdb_id"])

    op.execute(
        sa.text(
            """
            UPDATE movies_catalog mc
            SET imdb_id = mm.imdb_id
            FROM movies_metadata mm
            WHERE mm.tmdb_id = mc.tmdb_id
              AND mc.imdb_id IS NULL
              AND mm.imdb_id IS NOT NULL
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE series_catalog sc
            SET imdb_id = sm.imdb_id
            FROM series_metadata sm
            WHERE sm.tmdb_id = sc.tmdb_id
              AND sc.imdb_id IS NULL
              AND sm.imdb_id IS NOT NULL
            """
        )
    )


def downgrade() -> None:
    """Remove imdb_id columns and indexes."""
    op.drop_index("ix_series_catalog_imdb_id", table_name="series_catalog")
    op.drop_index("ix_movies_catalog_imdb_id", table_name="movies_catalog")
    op.drop_column("series_catalog", "imdb_id")
    op.drop_column("movies_catalog", "imdb_id")
