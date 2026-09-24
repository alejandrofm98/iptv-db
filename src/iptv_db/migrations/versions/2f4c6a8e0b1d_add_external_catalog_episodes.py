"""Persist external series episodes and background sync timestamps."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision: str = "2f4c6a8e0b1d"
down_revision: str | Sequence[str] | None = "c8e4f1a2b6d9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "external_catalog_items",
        sa.Column("localized_checked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "external_catalog_items",
        sa.Column("episodes_checked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "external_catalog_items",
        sa.Column("episodes_synced_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column("external_catalog_items", sa.Column("logo", sa.Text(), nullable=True))
    op.add_column("external_catalog_items", sa.Column("genres", JSONB(), nullable=True))
    op.add_column("external_catalog_items", sa.Column("cast", JSONB(), nullable=True))
    op.create_table(
        "external_catalog_episodes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("imdb_id", sa.String(length=20), nullable=False),
        sa.Column("season_number", sa.Integer(), nullable=False),
        sa.Column("episode_number", sa.Integer(), nullable=False),
        sa.Column("video_id", sa.Text(), nullable=False),
        sa.Column("title_es", sa.Text(), nullable=True),
        sa.Column("title_en", sa.Text(), nullable=True),
        sa.Column("overview_es", sa.Text(), nullable=True),
        sa.Column("overview_en", sa.Text(), nullable=True),
        sa.Column("thumbnail", sa.Text(), nullable=True),
        sa.Column("released", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "imdb_id",
            "season_number",
            "episode_number",
            name="uq_external_catalog_episode_identity",
        ),
    )
    op.create_index("ix_external_catalog_episodes_imdb", "external_catalog_episodes", ["imdb_id"])


def downgrade() -> None:
    op.drop_index("ix_external_catalog_episodes_imdb", table_name="external_catalog_episodes")
    op.drop_table("external_catalog_episodes")
    op.drop_column("external_catalog_items", "episodes_synced_at")
    op.drop_column("external_catalog_items", "episodes_checked_at")
    op.drop_column("external_catalog_items", "localized_checked_at")
    op.drop_column("external_catalog_items", "cast")
    op.drop_column("external_catalog_items", "genres")
    op.drop_column("external_catalog_items", "logo")
