"""add playback preferences

Revision ID: 5e8d9c1a2b3f
Revises: 0e2676090eed
Create Date: 2026-08-02 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "5e8d9c1a2b3f"
down_revision: str | Sequence[str] | None = "0e2676090eed"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Crea las preferencias de reproduccion por usuario y catalogo."""
    op.create_table(
        "playback_preferences",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("content_type", sa.String(length=20), nullable=False),
        sa.Column("catalog_id", sa.UUID(), nullable=False),
        sa.Column("audio_language", sa.String(length=32), nullable=True),
        sa.Column("audio_label", sa.String(length=255), nullable=True),
        sa.Column("subtitle_language", sa.String(length=32), nullable=True),
        sa.Column("subtitle_label", sa.String(length=255), nullable=True),
        sa.Column("subtitles_disabled", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "content_type IN ('movie', 'series')",
            name="ck_playback_preferences_content_type",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "content_type",
            "catalog_id",
            name="uq_playback_preferences_user_content",
        ),
    )


def downgrade() -> None:
    """Elimina las preferencias de reproduccion."""
    op.drop_table("playback_preferences")
