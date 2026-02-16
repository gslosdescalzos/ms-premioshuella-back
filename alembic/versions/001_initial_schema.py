"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-02-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profile",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("can_participate", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "category",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
    )

    op.create_table(
        "participation",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("profile_id", sa.String(36), sa.ForeignKey("profile.id"), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("category.id"), nullable=False),
        sa.Column("content_url", sa.Text(), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("is_scout", sa.Boolean(), nullable=True),
        sa.Column("scout_group", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("participant_name", sa.String(255), nullable=True),
        sa.Column("participant_surname", sa.String(255), nullable=True),
        sa.Column("is_finalist", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("submitted_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("profile_id", "category_id", name="uq_participation_profile_category"),
    )

    op.create_table(
        "initial_vote",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("profile_id", sa.String(36), sa.ForeignKey("profile.id"), nullable=False),
        sa.Column(
            "participation_id", sa.Integer(), sa.ForeignKey("participation.id"), nullable=False
        ),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("category.id"), nullable=False),
        sa.Column("creation_date", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("profile_id", "category_id", name="uq_initial_vote_profile_category"),
    )

    op.create_table(
        "newsletter",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("subscribed_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "contact",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("mensaje", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "colabora",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("nombre", sa.String(255), nullable=False),
        sa.Column("apellidos", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("telefono", sa.String(50), nullable=True),
        sa.Column("comentarios", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("colabora")
    op.drop_table("contact")
    op.drop_table("newsletter")
    op.drop_table("initial_vote")
    op.drop_table("participation")
    op.drop_table("category")
    op.drop_table("profile")
