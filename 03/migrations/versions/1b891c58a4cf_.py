"""empty message

Revision ID: 1b891c58a4cf
Revises: e0a6818f9848
Create Date: 2025-01-02 19:16:25.673392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b891c58a4cf'
down_revision = 'e0a6818f9848'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.alter_column('country',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('country',
               existing_type=sa.String(length=10),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)
        batch_op.drop_column('age')

    # ### end Alembic commands ###