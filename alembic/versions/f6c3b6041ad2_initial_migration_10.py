"""Initial migration 10

Revision ID: f6c3b6041ad2
Revises: d007123122b6
Create Date: 2024-03-10 20:52:20.328955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6c3b6041ad2'
down_revision: Union[str, None] = 'd007123122b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
