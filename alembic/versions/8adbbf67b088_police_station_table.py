"""police_station_table

Revision ID: 8adbbf67b088
Revises: 40cee7691a5f
Create Date: 2023-12-12 11:14:19.383461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '8adbbf67b088'
down_revision: Union[str, None] = '40cee7691a5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
  pass

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
 pass
    # ### end Alembic commands ###