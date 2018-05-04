"""empty message

Revision ID: 3bb7bd51f026
Revises: 808fe0be7170
Create Date: 2018-05-04 09:55:53.042757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bb7bd51f026'
down_revision = '808fe0be7170'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmedEmail', sa.String(length=6), nullable=True))
    op.drop_column('user', 'signingKey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('signingKey', sa.VARCHAR(length=100), nullable=True))
    op.drop_column('user', 'confirmedEmail')
    # ### end Alembic commands ###
