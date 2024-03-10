"""Initial migration 9

Revision ID: d007123122b6
Revises: a5b8469f1239
Create Date: 2024-03-10 20:39:25.004929

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd007123122b6'
down_revision: Union[str, None] = 'a5b8469f1239'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
