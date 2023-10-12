"""Add disabled field to User table

Revision ID: d31389c01700
Revises: 
Create Date: 2023-10-12 12:34:00.694107

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd31389c01700'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  
    op.add_column('user', sa.Column('disabled', sa.Boolean(), server_default='1'))



def downgrade() -> None:
    pass
    