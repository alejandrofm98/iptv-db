"""Persist external Cinemeta catalog items independently from IPTV content."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "c8e4f1a2b6d9"
down_revision: str | Sequence[str] | None = "a7b2c3d4e5f6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the provider-independent external catalog cache."""
    op.create_table(
        "external_catalog_items",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("content_type", sa.String(length=10), nullable=False),
        sa.Column("catalog_id", sa.String(length=50), nullable=False),
        sa.Column("catalog_position", sa.Integer(), nullable=False),
        sa.Column("imdb_id", sa.String(length=20), nullable=False),
        sa.Column("moviedb_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.Text(), nullable=True),
        sa.Column("title_es", sa.Text(), nullable=True),
        sa.Column("description_en", sa.Text(), nullable=True),
        sa.Column("overview_es", sa.Text(), nullable=True),
        sa.Column("poster", sa.Text(), nullable=True),
        sa.Column("backdrop", sa.Text(), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("imported_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "content_type",
            "catalog_id",
            "imdb_id",
            name="uq_external_catalog_items_identity",
        ),
    )
    op.create_index(
        "ix_external_catalog_items_type_catalog",
        "external_catalog_items",
        ["content_type", "catalog_id"],
    )
    op.create_index(
        "ix_external_catalog_items_type_imdb_id",
        "external_catalog_items",
        ["content_type", "imdb_id"],
    )
    op.create_index(
        "ix_external_catalog_items_type_catalog_position",
        "external_catalog_items",
        ["content_type", "catalog_id", "catalog_position"],
    )


def downgrade() -> None:
    """Drop the external catalog cache."""
    op.drop_index("ix_external_catalog_items_type_imdb_id", table_name="external_catalog_items")
    op.drop_index(
        "ix_external_catalog_items_type_catalog_position", table_name="external_catalog_items"
    )
    op.drop_index("ix_external_catalog_items_type_catalog", table_name="external_catalog_items")
    op.drop_table("external_catalog_items")
