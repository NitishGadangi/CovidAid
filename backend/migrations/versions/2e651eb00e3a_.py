"""empty message

Revision ID: 2e651eb00e3a
Revises: 65291d5edd48
Create Date: 2020-10-10 17:44:29.805072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e651eb00e3a'
down_revision = '65291d5edd48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('contact_number', sa.String(length=20), nullable=False),
    sa.Column('location', sa.String(length=80), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=False),
    sa.Column('subject', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('help_seeker', sa.Integer(), nullable=False),
    sa.Column('helper', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['help_seeker'], ['users.id'], ),
    sa.ForeignKeyConstraint(['helper'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('address'),
    sa.UniqueConstraint('contact_number'),
    sa.UniqueConstraint('description'),
    sa.UniqueConstraint('location'),
    sa.UniqueConstraint('subject')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###
