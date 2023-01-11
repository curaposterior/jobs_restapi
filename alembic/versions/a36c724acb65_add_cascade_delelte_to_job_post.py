"""add cascade delelte to job_post

Revision ID: a36c724acb65
Revises: d2de4cf66e65
Create Date: 2023-01-11 10:09:38.831598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a36c724acb65'
down_revision = 'd2de4cf66e65'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('job_post_skill_skill_id_fkey', 'job_post_skill', type_='foreignkey')
    op.drop_constraint('job_post_skill_job_post_id_fkey', 'job_post_skill', type_='foreignkey')
    op.create_foreign_key(None, 'job_post_skill', 'job_post', ['job_post_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'job_post_skill', 'skill', ['skill_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'job_post_skill', type_='foreignkey')
    op.drop_constraint(None, 'job_post_skill', type_='foreignkey')
    op.create_foreign_key('job_post_skill_job_post_id_fkey', 'job_post_skill', 'job_post', ['job_post_id'], ['id'])
    op.create_foreign_key('job_post_skill_skill_id_fkey', 'job_post_skill', 'skill', ['skill_id'], ['id'])
    # ### end Alembic commands ###
