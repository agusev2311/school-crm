"""empty message

Revision ID: e35e072f1dfd
Revises: 1b2210a21554
Create Date: 2025-03-16 13:45:28.274842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e35e072f1dfd'
down_revision = '1b2210a21554'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_approved', sa.Boolean(), server_default=sa.text("'true'::boolean"), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('submissions', schema=None) as batch_op:
        batch_op.drop_column('is_approved')

    # ### end Alembic commands ###
