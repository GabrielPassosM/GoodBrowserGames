"""empty message

Revision ID: 49fadf6e6195
Revises: ae3b439674a0
Create Date: 2022-05-27 16:31:33.700140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49fadf6e6195'
down_revision = 'ae3b439674a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('jogo_avaliado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('jogo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['jogo_id'], ['jogo.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jogo_avaliado')
    # ### end Alembic commands ###