"""first migrations

Revision ID: 0aaabd31b6e0
Revises: d5e4f235c2e0
Create Date: 2023-09-13 14:31:40.194832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0aaabd31b6e0'
down_revision: Union[str, None] = 'd5e4f235c2e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
