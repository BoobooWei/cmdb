"""empty message

Revision ID: 8f1b4f6a4443
Revises: 790411817c10
Create Date: 2016-08-01 16:30:37.343835

"""

# revision identifiers, used by Alembic.
revision = '8f1b4f6a4443'
down_revision = '790411817c10'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('racks', sa.Column('idc_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'racks_ibfk_1', 'racks', type_='foreignkey')
    op.create_foreign_key(None, 'racks', 'idcs', ['idc_id'], ['id'])
    op.drop_column('racks', 'idcname_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('racks', sa.Column('idcname_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'racks', type_='foreignkey')
    op.create_foreign_key(u'racks_ibfk_1', 'racks', 'idcs', ['idcname_id'], ['id'])
    op.drop_column('racks', 'idc_id')
    ### end Alembic commands ###