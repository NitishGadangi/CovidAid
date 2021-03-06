"""empty message

Revision ID: 97be1663d11c
Revises: 0f361ad4fc33
Create Date: 2020-10-07 23:17:59.855111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "97be1663d11c"
down_revision = "0f361ad4fc33"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=80), nullable=False),
        sa.Column("last_name", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("contact_number", sa.String(length=12), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("contact_number"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("first_name"),
        sa.UniqueConstraint("last_name"),
    )
    op.drop_table("user")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "username", sa.VARCHAR(length=80), autoincrement=False, nullable=False
        ),
        sa.Column("email", sa.VARCHAR(length=120), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
        sa.UniqueConstraint("email", name="user_email_key"),
        sa.UniqueConstraint("username", name="user_username_key"),
    )
    op.drop_table("users")
    # ### end Alembic commands ###
