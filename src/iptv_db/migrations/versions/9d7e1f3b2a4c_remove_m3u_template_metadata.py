"""Remove obsolete generated M3U metadata.

Revision ID: 9d7e1f3b2a4c
Revises: 71fffd6203e2
"""

from collections.abc import Sequence

from alembic import op

revision: str = "9d7e1f3b2a4c"
down_revision: str | Sequence[str] | None = "e5f6a8b9c0d1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # IF EXISTS: el grafo se linealizo despues de que algunas BD ya estaban
    # en e5f6a8b9c0d1, y las columnas pueden existir o no segun su historial.
    op.execute("ALTER TABLE sync_metadata DROP COLUMN IF EXISTS m3u_template_path")
    op.execute("ALTER TABLE sync_metadata DROP COLUMN IF EXISTS m3u_template_filename")
    op.execute("ALTER TABLE sync_metadata DROP COLUMN IF EXISTS m3u_size_mb")


def downgrade() -> None:
    raise RuntimeError("Generated M3U metadata is no longer supported")
