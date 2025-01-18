"""add ru and kg

Revision ID: 643901b31a7e
Revises: 2c7cb0e12094
Create Date: 2024-12-30 00:14:35.164346

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "643901b31a7e"
down_revision: Union[str, None] = "2c7cb0e12094"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "groups", ["title"])
    op.add_column("tickets", sa.Column("title_ru", sa.String(length=999), nullable=True))
    op.add_column("tickets", sa.Column("title_kg", sa.String(length=999), nullable=True))
    op.drop_column("tickets", "title")


def downgrade() -> None:
    op.add_column(
        "tickets",
        sa.Column("title", sa.VARCHAR(length=999), autoincrement=False, nullable=True),
    )
    op.drop_column("tickets", "title_kg")
    op.drop_column("tickets", "title_ru")
    op.drop_constraint(None, "groups", type_="unique")
