"""migration 12

Revision ID: f0856ee3e5b9
Revises: 54dbbbcfad1a
Create Date: 2024-03-10 23:42:10.014137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0856ee3e5b9'
down_revision: Union[str, None] = '54dbbbcfad1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
