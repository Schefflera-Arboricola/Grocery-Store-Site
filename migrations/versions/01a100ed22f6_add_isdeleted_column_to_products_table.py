"""Add isDeleted column to Products table

Revision ID: 01a100ed22f6
Revises: 
Create Date: 2023-08-03 14:40:03.429512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "01a100ed22f6"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.add_column(sa.Column("isDeleted", sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.drop_column("isDeleted")

    # ### end Alembic commands ###
