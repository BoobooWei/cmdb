"""empty message

Revision ID: 9aca554546b3
Revises: e9a0e817ae80
Create Date: 2016-05-28 16:49:48.722073

"""

# revision identifiers, used by Alembic.
revision = '9aca554546b3'
down_revision = 'e9a0e817ae80'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('instaff', sa.String(length=64), nullable=True))
    op.add_column('assets', sa.Column('intime', sa.DateTime(), nullable=True))
    op.add_column('assets', sa.Column('koriyasuendtime', sa.DateTime(), nullable=True))
    op.add_column('assets', sa.Column('koriyasustarttime', sa.DateTime(), nullable=True))
    op.add_column('assets', sa.Column('mainuses', sa.String(length=128), nullable=True))
    op.drop_column('assets', 'assettype')
    op.drop_column('assets', 'inputuser')
    op.drop_column('assets', 'inputtime')
    op.drop_column('assets', 'useasset')
    op.drop_column('assets', 'sinceendtime')
    op.drop_column('assets', 'sincestarttime')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('sincestarttime', mysql.DATETIME(), nullable=True))
    op.add_column('assets', sa.Column('sinceendtime', mysql.DATETIME(), nullable=True))
    op.add_column('assets', sa.Column('useasset', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('assets', sa.Column('inputtime', mysql.DATETIME(), nullable=True))
    op.add_column('assets', sa.Column('inputuser', mysql.VARCHAR(length=64), nullable=True))
    op.add_column('assets', sa.Column('assettype', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('assets', 'mainuses')
    op.drop_column('assets', 'koriyasustarttime')
    op.drop_column('assets', 'koriyasuendtime')
    op.drop_column('assets', 'intime')
    op.drop_column('assets', 'instaff')
    ### end Alembic commands ###