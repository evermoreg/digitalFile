"""empty message

Revision ID: 203e3bb15df9
Revises: e8b28f8eff96
Create Date: 2018-03-24 03:57:00.338451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '203e3bb15df9'
down_revision = 'e8b28f8eff96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('publicKey', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'publicKey')
    # ### end Alembic commands ###