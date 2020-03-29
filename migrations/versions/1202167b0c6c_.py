"""empty message

Revision ID: 1202167b0c6c
Revises: c04d758d6be4
Create Date: 2019-08-04 13:11:11.698088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1202167b0c6c'
down_revision = 'c04d758d6be4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ac_record', sa.Column('code', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ac_record', 'code')
    # ### end Alembic commands ###
