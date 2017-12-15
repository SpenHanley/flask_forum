"""empty message

Revision ID: eb4880e436df
Revises: d12d430b5532
Create Date: 2017-12-14 19:12:07.737391

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eb4880e436df'
down_revision = 'd12d430b5532'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('pinned', sa.Boolean(), nullable=False))
    op.drop_column('posts', 'is_pinned')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('is_pinned', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('posts', 'pinned')
    # ### end Alembic commands ###
