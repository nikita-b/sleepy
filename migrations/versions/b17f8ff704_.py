"""empty message

Revision ID: b17f8ff704
Revises: a4e42fbe84
Create Date: 2015-02-23 00:00:54.040990

"""

# revision identifiers, used by Alembic.
revision = 'b17f8ff704'
down_revision = 'a4e42fbe84'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article', 'url',
               existing_type=sa.VARCHAR(length=180),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article', 'url',
               existing_type=sa.VARCHAR(length=180),
               nullable=False)
    ### end Alembic commands ###