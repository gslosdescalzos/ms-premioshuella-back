"""participation_files table

Revision ID: 002
Revises: 001
Create Date: 2026-03-05

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("participation", "content_url")

    op.create_table(
        "participation_files",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("participation_id", sa.Integer(), sa.ForeignKey("participation.id"), nullable=False),
        sa.Column("profile_id", sa.String(36), sa.ForeignKey("profile.id"), nullable=False),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("category.id"), nullable=False),
        sa.Column("content_url", sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("participation_files")
    op.add_column(
        "participation",
        sa.Column("content_url", sa.Text(), nullable=True),
    )
