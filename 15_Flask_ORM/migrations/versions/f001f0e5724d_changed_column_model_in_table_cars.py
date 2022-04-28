"""Changed column model in table cars

Revision ID: f001f0e5724d
Revises: 6593b289b055
Create Date: 2022-03-31 15:22:10.973331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f001f0e5724d'
down_revision = '6593b289b055'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cars', 'model',
               existing_type=sa.VARCHAR(length=150),
               type_=sa.String(length=30),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cars', 'model',
               existing_type=sa.String(length=30),
               type_=sa.VARCHAR(length=150),
               existing_nullable=False)
    # ### end Alembic commands ###