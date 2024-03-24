"""migration 13

Revision ID: 7e724f41eb74
Revises: f0856ee3e5b9
Create Date: 2024-03-24 11:36:40.907535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e724f41eb74'
down_revision: Union[str, None] = 'f0856ee3e5b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
