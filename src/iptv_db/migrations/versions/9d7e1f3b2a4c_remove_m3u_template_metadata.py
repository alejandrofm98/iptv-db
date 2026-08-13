"""Remove obsolete generated M3U metadata.

Revision ID: 9d7e1f3b2a4c
Revises: 71fffd6203e2
"""

from collections.abc import Sequence

from alembic import op

revision: str = "9d7e1f3b2a4c"
down_revision: str | Sequence[str] | None = "71fffd6203e2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("sync_metadata", "m3u_template_path")
    op.drop_column("sync_metadata", "m3u_template_filename")
    op.drop_column("sync_metadata", "m3u_size_mb")


def downgrade() -> None:
    raise RuntimeError("Generated M3U metadata is no longer supported")
