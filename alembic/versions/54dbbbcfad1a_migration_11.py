"""migration 11

Revision ID: 54dbbbcfad1a
Revises: f6c3b6041ad2
Create Date: 2024-03-10 23:35:27.803261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54dbbbcfad1a'
down_revision: Union[str, None] = 'f6c3b6041ad2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
