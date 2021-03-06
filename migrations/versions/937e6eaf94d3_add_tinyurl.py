"""add tinyurl

Revision ID: 937e6eaf94d3
Revises: 32c4874ba2dd
Create Date: 2019-12-12 00:49:21.074601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '937e6eaf94d3'
down_revision = '32c4874ba2dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tinyurl',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('long_url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tinyurl')
    # ### end Alembic commands ###
