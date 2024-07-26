"""migration2:ADD_COLUMN_SPEED

Revision ID: 8d46c0395613
Revises: 27e1a13f70fb
Create Date: 2024-06-28 01:42:55.985054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d46c0395613'
down_revision: Union[str, None] = '27e1a13f70fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("CorrectSpaceships", sa.Column('speed', sa.FLOAT))


def downgrade() -> None:
    op.drop_column("CorrectSpaceships", 'speed')
