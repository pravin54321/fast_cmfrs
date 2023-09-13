"""add new fields to PersonModel

Revision ID: ef7d2816ed4e
Revises: 8cf510201cac
Create Date: 2023-09-13 14:27:54.601723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef7d2816ed4e'
down_revision: Union[str, None] = '8cf510201cac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
