"""new field power

Revision ID: b39b8d3c77f0
Revises: 357d6ebcfadf
Create Date:

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'b39b8d3c77f0'  # (1)
down_revision = '357d6ebcfadf'  # (2)
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hero', sa.Column('power', sa.Integer(), nullable=True))  # (3)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hero', 'power')  # (4)
    # ### end Alembic commands ###
