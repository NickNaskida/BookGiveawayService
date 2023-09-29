"""author unique

Revision ID: dd93cf96037f
Revises: e26b4a09715e
Create Date: 2023-09-26 23:28:36.457368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd93cf96037f'
down_revision: Union[str, None] = 'e26b4a09715e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('authors', 'full_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
    op.create_unique_constraint(None, 'authors', ['full_name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'authors', type_='unique')
    op.alter_column('authors', 'full_name',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###