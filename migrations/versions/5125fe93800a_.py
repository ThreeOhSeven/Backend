"""empty message

Revision ID: 5125fe93800a
Revises: d8b134d692ed
Create Date: 2017-12-01 00:02:02.469743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5125fe93800a'
down_revision = 'd8b134d692ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('photo_url', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Users', 'photo_url')
    # ### end Alembic commands ###
