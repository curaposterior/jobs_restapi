"""add cascade 3

Revision ID: be2e24a06128
Revises: 59a2d5a589e9
Create Date: 2023-01-11 21:58:38.884466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be2e24a06128'
down_revision = '59a2d5a589e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employee_profile_company_fkey', 'employee_profile', type_='foreignkey')
    op.create_foreign_key(None, 'employee_profile', 'company', ['company'], ['company_name'])
    op.drop_constraint('employee_skills_user_id_fkey', 'employee_skills', type_='foreignkey')
    op.create_foreign_key(None, 'employee_skills', 'employee_profile', ['user_id'], ['user_id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'employee_skills', type_='foreignkey')
    op.create_foreign_key('employee_skills_user_id_fkey', 'employee_skills', 'employee_profile', ['user_id'], ['user_id'])
    op.drop_constraint(None, 'employee_profile', type_='foreignkey')
    op.create_foreign_key('employee_profile_company_fkey', 'employee_profile', 'company', ['company'], ['company_name'], ondelete='CASCADE')
    # ### end Alembic commands ###
