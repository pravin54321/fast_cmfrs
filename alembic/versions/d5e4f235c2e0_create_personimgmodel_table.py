"""Create PersonImgModel table

Revision ID: d5e4f235c2e0
Revises: ef7d2816ed4e
Create Date: 2023-09-13 14:30:15.796704

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5e4f235c2e0'
down_revision: Union[str, None] = 'ef7d2816ed4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
