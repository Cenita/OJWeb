"""empty message

Revision ID: 4e82ae76e657
Revises: b344acf0b9fc
Create Date: 2019-08-03 15:38:10.421797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e82ae76e657'
down_revision = 'b344acf0b9fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question', sa.Column('example', sa.Text(), nullable=True))
    op.add_column('question', sa.Column('tips', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question', 'tips')
    op.drop_column('question', 'example')
    # ### end Alembic commands ###
