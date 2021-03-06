"""notifications

Revision ID: 61295638e438
Revises: fffc079e3f9a
Create Date: 2019-11-28 00:02:39.774301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61295638e438'
down_revision = 'fffc079e3f9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notificaion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notificaion_name'), 'notificaion', ['name'], unique=False)
    op.create_index(op.f('ix_notificaion_timestamp'), 'notificaion', ['timestamp'], unique=False)
    op.create_table('task',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('complete', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_task_name'), 'task', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_task_name'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_notificaion_timestamp'), table_name='notificaion')
    op.drop_index(op.f('ix_notificaion_name'), table_name='notificaion')
    op.drop_table('notificaion')
    # ### end Alembic commands ###
