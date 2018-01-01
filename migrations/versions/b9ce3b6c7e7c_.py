"""empty message

Revision ID: b9ce3b6c7e7c
Revises: 8ea3ab48d226
Create Date: 2017-12-08 13:12:19.238877

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9ce3b6c7e7c'
down_revision = '8ea3ab48d226'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['profile_route'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###