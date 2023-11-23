"""group_image

Revision ID: 44ad1b05dbb2
Revises: d31389c01700
Create Date: 2023-11-23 18:07:45.825600

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '44ad1b05dbb2'
down_revision: Union[str, None] = 'd31389c01700'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'groupimg',
        sa.Column('id',sa.Integer,primary_key = True),
        sa.Column('ImgPath',sa.String(200))
    )


def downgrade() -> None:
    pass
