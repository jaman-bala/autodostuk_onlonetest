"""up: fix

Revision ID: 7d304411127f
Revises: b566f8ecd505
Create Date: 2024-12-30 01:14:57.535669

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7d304411127f"
down_revision: Union[str, None] = "b566f8ecd505"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("answers", sa.Column("title_ru", sa.String(length=999), nullable=True))
    op.add_column("answers", sa.Column("title_kg", sa.String(length=999), nullable=True))
    op.drop_column("answers", "title")
    op.add_column("tickets", sa.Column("title", sa.String(length=999), nullable=True))
    op.drop_column("tickets", "title_kg")
    op.drop_column("tickets", "title_ru")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.add_column(
        "tickets",
        sa.Column("title_ru", sa.VARCHAR(length=999), autoincrement=False, nullable=True),
    )
    op.add_column(
        "tickets",
        sa.Column("title_kg", sa.VARCHAR(length=999), autoincrement=False, nullable=True),
    )
    op.drop_column("tickets", "title")
    op.add_column(
        "answers",
        sa.Column("title", sa.VARCHAR(length=999), autoincrement=False, nullable=True),
    )
    op.drop_column("answers", "title_kg")
    op.drop_column("answers", "title_ru")
