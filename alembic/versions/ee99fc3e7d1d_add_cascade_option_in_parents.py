"""add_cascade_option_in_parents

Revision ID: ee99fc3e7d1d
Revises: fcf77e7f43f4
Create Date: 2023-10-06 12:53:43.439721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ee99fc3e7d1d'
down_revision: Union[str, None] = 'fcf77e7f43f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_personimg_id', table_name='personimg')
    op.drop_table('personimg')
    op.drop_index('Email', table_name='person')
    op.drop_index('ix_person_id', table_name='person')
    op.drop_table('person')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('Name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('Mobile_Number', mysql.VARCHAR(length=12), nullable=True),
    sa.Column('Email', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('Age', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('Gender', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('Address', mysql.TEXT(), nullable=True),
    sa.Column('Status', mysql.VARCHAR(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_person_id', 'person', ['id'], unique=False)
    op.create_index('Email', 'person', ['Email'], unique=False)
    op.create_table('personimg',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('file_path', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('face_encoding', mysql.TEXT(), nullable=True),
    sa.Column('Person_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['Person_id'], ['person.id'], name='personimg_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_general_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('ix_personimg_id', 'personimg', ['id'], unique=False)
    # ### end Alembic commands ###
