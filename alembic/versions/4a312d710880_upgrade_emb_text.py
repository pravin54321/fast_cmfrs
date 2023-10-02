"""upgrade emb_text

Revision ID: 4a312d710880
Revises: 
Create Date: 2023-09-28 13:04:19.371613

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a312d710880'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.alter_column('personimg', 'face_encoding', type_=sa.Text())



def downgrade() -> None:
    pass
