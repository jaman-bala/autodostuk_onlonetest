"""Добавлено каскадное удаление в UserOrm

Revision ID: 08a36e3d8297
Revises: 95ed7c3653c7
Create Date: 2024-12-30 09:54:42.284052

"""

from typing import Sequence, Union

from alembic import op


revision: str = "08a36e3d8297"
down_revision: Union[str, None] = "95ed7c3653c7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("users_group_id_fkey", "users", type_="foreignkey")
    op.create_foreign_key(None, "users", "groups", ["group_id"], ["id"], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="foreignkey")
    op.create_foreign_key("users_group_id_fkey", "users", "groups", ["group_id"], ["id"])
