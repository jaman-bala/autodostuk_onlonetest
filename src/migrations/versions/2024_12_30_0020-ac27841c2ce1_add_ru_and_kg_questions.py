"""add ru and kg questions

Revision ID: ac27841c2ce1
Revises: 643901b31a7e
Create Date: 2024-12-30 00:20:53.422678

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ac27841c2ce1"
down_revision: Union[str, None] = "643901b31a7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("questions", sa.Column("title_ru", sa.String(length=999), nullable=True))
    op.add_column("questions", sa.Column("title_kg", sa.String(length=999), nullable=True))
    op.add_column("questions", sa.Column("description_ru", sa.String(), nullable=True))
    op.add_column("questions", sa.Column("description_kg", sa.String(), nullable=True))
    op.drop_column("questions", "description")
    op.drop_column("questions", "title")


def downgrade() -> None:
    op.add_column(
        "questions",
        sa.Column("title", sa.VARCHAR(length=999), autoincrement=False, nullable=True),
    )
    op.add_column(
        "questions",
        sa.Column("description", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_column("questions", "description_kg")
    op.drop_column("questions", "description_ru")
    op.drop_column("questions", "title_kg")
    op.drop_column("questions", "title_ru")
