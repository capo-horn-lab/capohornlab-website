"""Create newsletter tables: subscribers, campaigns, sends.

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-22
"""

from typing import Final

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision: Final[str] = "0003"
down_revision: str | None = "0002"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    # ── newsletter_subscribers ──
    op.create_table(
        "newsletter_subscribers",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("name", sa.String(150), nullable=True),
        sa.Column("user_id", UUID(), nullable=True),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("verification_token", sa.String(128), nullable=True),
        sa.Column("unsubscribed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column(
            "subscribed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        op.f("ix_newsletter_subscribers_email"),
        "newsletter_subscribers",
        ["email"],
        unique=True,
    )
    op.create_index(
        op.f("ix_newsletter_subscribers_verification_token"),
        "newsletter_subscribers",
        ["verification_token"],
        unique=True,
    )

    # ── newsletter_campaigns ──
    op.create_table(
        "newsletter_campaigns",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("content_html", sa.Text(), nullable=False),
        sa.Column("content_text", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(30),
            nullable=False,
            server_default="bozza",
        ),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_by", UUID(), nullable=True),
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
            ["created_by"],
            ["users.id"],
            ondelete="SET NULL",
        ),
    )
    op.create_index(
        op.f("ix_newsletter_campaigns_status"),
        "newsletter_campaigns",
        ["status"],
    )

    # ── newsletter_sends ──
    op.create_table(
        "newsletter_sends",
        sa.Column("id", UUID(), nullable=False),
        sa.Column("campaign_id", UUID(), nullable=False),
        sa.Column("subscriber_id", UUID(), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("opened_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(
            ["campaign_id"],
            ["newsletter_campaigns.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["subscriber_id"],
            ["newsletter_subscribers.id"],
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint(
            "campaign_id", "subscriber_id",
            name="uq_campaign_subscriber",
        ),
    )
    op.create_index(
        op.f("ix_newsletter_sends_campaign_id"),
        "newsletter_sends",
        ["campaign_id"],
    )
    op.create_index(
        op.f("ix_newsletter_sends_subscriber_id"),
        "newsletter_sends",
        ["subscriber_id"],
    )


def downgrade() -> None:
    op.drop_table("newsletter_sends")
    op.drop_table("newsletter_campaigns")
    op.drop_table("newsletter_subscribers")
