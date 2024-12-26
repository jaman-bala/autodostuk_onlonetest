"""add User models last_login

Revision ID: db27f0cec294
Revises: 96ed30a1b7f8
Create Date: 2024-12-22 20:50:45.373816

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "db27f0cec294"
down_revision: Union[str, None] = "96ed30a1b7f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_login", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_login")
