"""Create live_snapshots table.

Revision ID: 0005
Revises: 0004
"""
from typing import Final

import sqlalchemy as sa
from alembic import op

revision: Final[str] = "0005"
down_revision: str | None = "0004"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    op.create_table(
        "live_snapshots",
        sa.Column("chiave", sa.String(length=32), nullable=False),
        sa.Column("ricevuto", sa.String(length=32), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("byte", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("chiave"),
    )


def downgrade() -> None:
    op.drop_table("live_snapshots")
