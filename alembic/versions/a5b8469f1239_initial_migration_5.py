"""Initial migration 5

Revision ID: a5b8469f1239
Revises: 65fc8541a9d2
Create Date: 2024-03-10 20:37:36.666296

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5b8469f1239'
down_revision: Union[str, None] = '65fc8541a9d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
