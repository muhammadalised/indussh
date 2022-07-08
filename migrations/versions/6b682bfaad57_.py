"""empty message

Revision ID: 6b682bfaad57
Revises: 2e72e9912e34
Create Date: 2022-07-08 17:44:45.432794

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6b682bfaad57'
down_revision = '2e72e9912e34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orderitems', sa.Column('price', sa.Integer(), nullable=False))
    op.drop_column('orderitems', 'discounted_price')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orderitems', sa.Column('discounted_price', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('orderitems', 'price')
    # ### end Alembic commands ###
