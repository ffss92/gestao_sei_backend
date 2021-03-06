"""Vários destinos a um processo

Revision ID: 2a0f547a395c
Revises: 611f1ff72af5
Create Date: 2021-12-27 16:24:42.936916

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2a0f547a395c'
down_revision = '611f1ff72af5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('process_destination',
    sa.Column('process_id', sa.Integer(), nullable=True),
    sa.Column('destination_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['destination_id'], ['destination.id'], ),
    sa.ForeignKeyConstraint(['process_id'], ['process.id'], )
    )
    op.add_column('process', sa.Column('due_to', sa.DateTime(), nullable=True))
    op.drop_constraint('process_ibfk_2', 'process', type_='foreignkey')
    op.drop_column('process', 'destination_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('process', sa.Column('destination_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('process_ibfk_2', 'process', 'destination', ['destination_id'], ['id'], ondelete='SET NULL')
    op.drop_column('process', 'due_to')
    op.drop_table('process_destination')
    # ### end Alembic commands ###
