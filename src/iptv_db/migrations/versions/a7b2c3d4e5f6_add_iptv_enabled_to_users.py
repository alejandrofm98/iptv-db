"""Allow WalacTV accounts without an IPTV provider."""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a7b2c3d4e5f6"
down_revision: str | Sequence[str] | None = "f3a1c9e2b4d5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "iptv_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "iptv_enabled")
