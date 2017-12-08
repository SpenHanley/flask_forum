"""empty message

Revision ID: 39a95c52d03b
Revises: 
Create Date: 2017-12-08 08:27:49.548829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39a95c52d03b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('error', sa.String(length=16), nullable=True),
    sa.Column('details', sa.String(length=128), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('route', sa.String(length=8), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('is_pinned', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('route')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.Column('confirmed_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipient', sa.Integer(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=64), nullable=False),
    sa.Column('message', sa.String(length=256), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('sent', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('description', sa.String(length=192), nullable=True),
    sa.Column('content', sa.String(length=1024), nullable=True),
    sa.Column('route', sa.String(length=8), nullable=True),
    sa.Column('sub_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('anonymous', sa.Boolean(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('is_pinned', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sub_id'], ['subs.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('route')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.Integer(), nullable=True),
    sa.Column('content', sa.String(length=256), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('posts')
    op.drop_table('messages')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('subs')
    op.drop_table('logs')
    # ### end Alembic commands ###
