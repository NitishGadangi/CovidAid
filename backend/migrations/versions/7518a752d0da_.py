"""empty message

Revision ID: 7518a752d0da
Revises: 2b1375f344ae
Create Date: 2020-10-08 00:04:51.176281

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7518a752d0da"
down_revision = "2b1375f344ae"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "password", existing_type=sa.VARCHAR(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "password", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###
