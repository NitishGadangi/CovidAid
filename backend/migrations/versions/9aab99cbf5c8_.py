"""empty message

Revision ID: 9aab99cbf5c8
Revises: 97be1663d11c
Create Date: 2020-10-07 23:59:37.393430

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9aab99cbf5c8"
down_revision = "97be1663d11c"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("users_first_name_key", "users", type_="unique")
    op.drop_constraint("users_last_name_key", "users", type_="unique")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("users_last_name_key", "users", ["last_name"])
    op.create_unique_constraint("users_first_name_key", "users", ["first_name"])
    # ### end Alembic commands ###
