"""add extra column

Revision ID: 5d7de3d3b0bf
Revises: 44ad1b05dbb2
Create Date: 2023-11-28 11:48:02.237903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d7de3d3b0bf'
down_revision: Union[str, None] = '44ad1b05dbb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('groupimg',sa.Column('original_img',sa.String(200)))
    


def downgrade() -> None:
    op.drop_column('groupimg','original_img')
