"""add hidden channel groups

Revision ID: 7f3a9c1e4b2d
Revises: 9d7e1f3b2a4c
Create Date: 2026-09-09 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "7f3a9c1e4b2d"
down_revision: str | Sequence[str] | None = "9d7e1f3b2a4c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Crea los grupos de canales ocultos por usuario (alcance grupo + pais).

    country == "" significa global (todos los paises). Se usa cadena vacia
    en vez de NULL para que la PK (user_id, country, group_name) sea efectiva.
    """
    op.create_table(
        "hidden_channel_groups",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("country", sa.String(length=10), nullable=False, server_default=""),
        sa.Column("group_name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "country", "group_name"),
    )


def downgrade() -> None:
    """Elimina los grupos de canales ocultos."""
    op.drop_table("hidden_channel_groups")
