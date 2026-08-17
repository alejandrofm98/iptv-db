"""Add torrent_languages classification to catalog content."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "e5f6a8b9c0d1"
down_revision: str | Sequence[str] | None = "d9a2b7c4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add torrent_languages (JSONB) to catalog tables and episodes."""
    for table in ("movies_catalog", "series_catalog", "series_episodes"):
        op.add_column(
            table,
            sa.Column("torrent_languages", JSONB(), nullable=True),
        )


def downgrade() -> None:
    """Remove torrent_languages column."""
    for table in ("series_episodes", "series_catalog", "movies_catalog"):
        op.drop_column(table, "torrent_languages")
