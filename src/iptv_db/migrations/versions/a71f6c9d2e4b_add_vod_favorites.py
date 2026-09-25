"""Add account-scoped movie and series favorites."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a71f6c9d2e4b"
down_revision: str | Sequence[str] | None = "7f3a9c1e4b2d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create the per-user VOD favorites table."""
    op.create_table(
        "vod_favorites",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("content_type", sa.String(length=10), nullable=False),
        sa.Column("content_id", sa.String(length=255), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.CheckConstraint("content_type IN ('movies', 'series')", name="ck_vod_favorites_type"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "content_type", "content_id"),
    )
    op.create_index("ix_vod_favorites_user_created", "vod_favorites", ["user_id", "created_at"])


def downgrade() -> None:
    """Remove the per-user VOD favorites table."""
    op.drop_index("ix_vod_favorites_user_created", table_name="vod_favorites")
    op.drop_table("vod_favorites")
