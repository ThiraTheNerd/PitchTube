"""Remove the categories class

Revision ID: edeffbff6a7a
Revises: af6524bbc696
Create Date: 2021-06-16 16:50:49.562824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edeffbff6a7a'
down_revision = 'af6524bbc696'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('categories')
    op.drop_constraint('pitches_category_id_fkey', 'pitches', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('pitches_category_id_fkey', 'pitches', 'categories', ['category_id'], ['id'])
    op.create_table('categories',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('category_name', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='categories_pkey')
    )
    # ### end Alembic commands ###
