"""subdivision_add_table

Revision ID: 72f94b4ab7ec
Revises: 1cb17b6e743d
Create Date: 2023-12-11 12:24:56.864004

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '72f94b4ab7ec'
down_revision: Union[str, None] = '1cb17b6e743d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
   pass