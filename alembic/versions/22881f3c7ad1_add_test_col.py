"""add test col

Revision ID: 22881f3c7ad1
Revises: 79fb9454d0fa
Create Date: 2022-11-22 23:28:00.059925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22881f3c7ad1'
down_revision = '79fb9454d0fa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('test_col', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'test_col')
    # ### end Alembic commands ###
