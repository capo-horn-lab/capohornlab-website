"""Create strategy_requests, status_history, attachments, internal_notes tables.

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-22
"""

from typing import Final

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB, UUID

revision: Final[str] = "0002"
down_revision: str | None = "0001"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    # ── Create request_status enum ──
    op.execute(
        "CREATE TYPE request_status AS ENUM ("
        "'inviata', 'info_mancanti', 'in_valutazione', "
        "'accettata', 'rifiutata', 'in_lavorazione', 'completata'"
        ")"
    )

    # ── strategy_requests ──
    op.create_table(
        "strategy_requests",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("user_id", UUID(), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "inviata",
                "info_mancanti",
                "in_valutazione",
                "accettata",
                "rifiutata",
                "in_lavorazione",
                "completata",
                name="request_status",
            ),
            nullable=False,
            server_default="inviata",
        ),
        # Strategy identity
        sa.Column("strategy_name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("instrument", sa.String(50), nullable=False),
        # Time settings
        sa.Column("timeframe", sa.String(30), nullable=True),
        sa.Column("historical_period", sa.String(100), nullable=True),
        sa.Column("session_times", sa.String(200), nullable=True),
        # Rules
        sa.Column("entry_rules_long", sa.Text(), nullable=True),
        sa.Column("entry_rules_short", sa.Text(), nullable=True),
        sa.Column("exit_rules", sa.Text(), nullable=True),
        sa.Column("stop_loss", sa.String(100), nullable=True),
        sa.Column("take_profit", sa.String(100), nullable=True),
        sa.Column("trailing_stop", sa.String(100), nullable=True),
        sa.Column("break_even", sa.String(100), nullable=True),
        # Parameters
        sa.Column("indicators_params", JSONB(), nullable=True),
        sa.Column("contracts", sa.Integer(), nullable=True),
        sa.Column("commission_slippage", sa.Text(), nullable=True),
        sa.Column("additional_notes", sa.Text(), nullable=True),
        # Admin fields
        sa.Column("admin_notes", sa.Text(), nullable=True),
        sa.Column("clarification_request", sa.Text(), nullable=True),
        # Timestamps
        sa.Column(
            "submitted_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("evaluated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        op.f("ix_strategy_requests_user_id"),
        "strategy_requests",
        ["user_id"],
    )
    op.create_index(
        op.f("ix_strategy_requests_status"),
        "strategy_requests",
        ["status"],
    )

    # ── status_history ──
    op.create_table(
        "status_history",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("request_id", UUID(), nullable=False),
        sa.Column("from_status", sa.String(30), nullable=True),
        sa.Column("to_status", sa.String(30), nullable=False),
        sa.Column("changed_by", UUID(), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["strategy_requests.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["changed_by"],
            ["users.id"],
        ),
    )
    op.create_index(
        op.f("ix_status_history_request_id"),
        "status_history",
        ["request_id"],
    )

    # ── attachments ──
    op.create_table(
        "attachments",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("request_id", UUID(), nullable=False),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("original_name", sa.String(255), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("storage_path", sa.String(500), nullable=False),
        sa.Column(
            "uploaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["strategy_requests.id"],
            ondelete="CASCADE",
        ),
    )
    op.create_index(
        op.f("ix_attachments_request_id"),
        "attachments",
        ["request_id"],
    )

    # ── internal_notes ──
    op.create_table(
        "internal_notes",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("request_id", UUID(), nullable=False),
        sa.Column("author_id", UUID(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["request_id"],
            ["strategy_requests.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["users.id"],
        ),
    )
    op.create_index(
        op.f("ix_internal_notes_request_id"),
        "internal_notes",
        ["request_id"],
    )


def downgrade() -> None:
    op.drop_table("internal_notes")
    op.drop_table("attachments")
    op.drop_table("status_history")
    op.drop_table("strategy_requests")
    op.execute("DROP TYPE IF EXISTS request_status")
