"""preinscription table

Revision ID: 003
Revises: 002
Create Date: 2026-04-07

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "preinscription",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("profile_id", sa.String(length=36), sa.ForeignKey("profile.id"), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=False),
        sa.Column("surname", sa.String(length=255), nullable=True),
        sa.Column("categories", sa.JSON(), nullable=False),
        sa.Column("is_scout_group", sa.Boolean(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("profile_id", name="uq_preinscription_profile"),
    )


def downgrade() -> None:
    op.drop_table("preinscription")