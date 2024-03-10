"""Initial migration 3

Revision ID: 65fc8541a9d2
Revises: 4220298884f5
Create Date: 2024-03-10 20:37:05.638194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65fc8541a9d2'
down_revision: Union[str, None] = '4220298884f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
