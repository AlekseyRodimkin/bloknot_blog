"""Changed telegram user

Revision ID: bb035e406f84
Revises: 5159f6ead79a
Create Date: 2024-08-30 17:03:08.897745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb035e406f84'
down_revision = '5159f6ead79a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('ix_user_telegram')
        batch_op.create_index(batch_op.f('ix_user_telegram'), ['telegram'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_telegram'))
        batch_op.create_index('ix_user_telegram', ['telegram'], unique=1)

    # ### end Alembic commands ###
