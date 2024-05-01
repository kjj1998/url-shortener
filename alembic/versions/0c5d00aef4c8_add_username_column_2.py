"""Add username column 2

Revision ID: 0c5d00aef4c8
Revises: 6a3f6a462cb1
Create Date: 2024-04-20 23:13:06.797798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c5d00aef4c8'
down_revision: Union[str, None] = '6a3f6a462cb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("url", sa.Column("username", sa.String(), nullable=True), schema='shortener_schema')
    pass


def downgrade() -> None:
    op.drop_column("url", "username", schema='shortener_schema')
    pass
