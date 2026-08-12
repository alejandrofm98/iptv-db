"""Add IPTV and torrent source state to catalog content."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d9a2b7c4e5f6"
down_revision: str | Sequence[str] | None = "c4d8e2f1a907"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Add source flags without changing existing catalog identity."""
    for table in ("movies_catalog", "series_catalog"):
        op.add_column(
            table,
            sa.Column(
                "has_iptv_source",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("false"),
            ),
        )
        op.add_column(
            table,
            sa.Column(
                "has_torrent_source",
                sa.Boolean(),
                nullable=False,
                server_default=sa.text("false"),
            ),
        )
        op.add_column(
            table,
            sa.Column("torrent_source_checked_at", sa.DateTime(timezone=True), nullable=True),
        )

    op.add_column(
        "series_episodes",
        sa.Column("has_iptv_source", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column(
        "series_episodes",
        sa.Column(
            "has_torrent_source", sa.Boolean(), nullable=False, server_default=sa.text("false")
        ),
    )
    op.add_column(
        "series_episodes",
        sa.Column("torrent_source_checked_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.execute(
        sa.text(
            """
            UPDATE movies_catalog mc
            SET has_iptv_source = EXISTS (
                SELECT 1 FROM movie_streams ms WHERE ms.movie_id = mc.id
            )
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE series_catalog sc
            SET has_iptv_source = EXISTS (
                SELECT 1
                FROM series_episodes se
                JOIN series_streams ss ON ss.episode_id = se.id
                WHERE se.catalog_id = sc.id
            )
            """
        )
    )
    op.execute(
        sa.text(
            """
            UPDATE series_episodes se
            SET has_iptv_source = EXISTS (
                SELECT 1 FROM series_streams ss WHERE ss.episode_id = se.id
            )
            """
        )
    )


def downgrade() -> None:
    """Remove source flags."""
    for table in ("series_episodes", "series_catalog", "movies_catalog"):
        op.drop_column(table, "torrent_source_checked_at")
        op.drop_column(table, "has_torrent_source")
        op.drop_column(table, "has_iptv_source")
