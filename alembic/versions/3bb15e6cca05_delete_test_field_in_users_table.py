"""delete test field in users table

Revision ID: 3bb15e6cca05
Revises: 06f4fe3d2871
Create Date: 2022-11-23 20:46:37.019279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bb15e6cca05'
down_revision = '06f4fe3d2871'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'test_col')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('test_col', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###