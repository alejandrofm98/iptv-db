"""Add episode IMDb IDs and cached IntroDB video segments."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c4d8e2f1a907"
down_revision: str | Sequence[str] | None = "5e8d9c1a2b3f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the IntroDB cache schema."""
    op.add_column("series_episodes", sa.Column("imdb_id", sa.String(length=20), nullable=True))
    op.create_index("ix_series_episodes_imdb_id", "series_episodes", ["imdb_id"])

    op.create_table(
        "video_segment_sync",
        sa.Column("episode_id", sa.UUID(), nullable=False),
        sa.Column("source", sa.String(length=30), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("not_found", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.ForeignKeyConstraint(["episode_id"], ["series_episodes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("episode_id", "source"),
    )

    op.create_table(
        "video_segments",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("episode_id", sa.UUID(), nullable=False),
        sa.Column("segment_type", sa.String(length=10), nullable=False),
        sa.Column("start_ms", sa.BigInteger(), nullable=False),
        sa.Column("end_ms", sa.BigInteger(), nullable=False),
        sa.Column("confidence", sa.Numeric(precision=4, scale=3), nullable=True),
        sa.Column("submission_count", sa.Integer(), nullable=True),
        sa.Column("source", sa.String(length=30), nullable=False),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["episode_id"], ["series_episodes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("episode_id", "segment_type", "source"),
        sa.CheckConstraint("segment_type IN ('intro', 'recap', 'outro')"),
        sa.CheckConstraint("start_ms >= 0"),
        sa.CheckConstraint("end_ms > start_ms"),
    )


def downgrade() -> None:
    """Drop the IntroDB cache schema."""
    op.drop_table("video_segments")
    op.drop_table("video_segment_sync")
    op.drop_index("ix_series_episodes_imdb_id", table_name="series_episodes")
    op.drop_column("series_episodes", "imdb_id")
