"""empty message

Revision ID: c04d758d6be4
Revises: 76473bb85b6c
Create Date: 2019-08-04 11:33:31.266973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c04d758d6be4'
down_revision = '76473bb85b6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('luogu',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('token', sa.Text(), nullable=True),
    sa.Column('cookies', sa.Text(), nullable=True),
    sa.Column('update_time', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('luogu')
    # ### end Alembic commands ###