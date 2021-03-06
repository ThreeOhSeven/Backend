"""empty message

Revision ID: 216e7bdd51b1
Revises: 393685c0511f
Create Date: 2017-11-08 23:56:03.090412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '216e7bdd51b1'
down_revision = '393685c0511f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AddressBook',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('account_hex', sa.Text(), nullable=False),
    sa.Column('bc_passphrase', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['Users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('AddressBook')
    # ### end Alembic commands ###
