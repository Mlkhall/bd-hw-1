"""drop_cols

Revision ID: f19a8e474ada
Revises: f87a7a0e790a
Create Date: 2024-02-11 20:25:46.833725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f19a8e474ada'
down_revision: Union[str, None] = 'f87a7a0e790a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction_n3', 'product_size')
    op.drop_column('transaction_n3', 'list_price')
    op.drop_column('transaction_n3', 'product_line')
    op.drop_column('transaction_n3', 'product_class')
    op.drop_column('transaction_n3', 'brand')
    op.drop_column('transaction_n3', 'standard_cost')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction_n3', sa.Column('standard_cost', sa.NUMERIC(), autoincrement=False, nullable=True))
    op.add_column('transaction_n3', sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('transaction_n3', sa.Column('product_class', postgresql.ENUM('medium', 'high', 'low', name='product_class'), autoincrement=False, nullable=True))
    op.add_column('transaction_n3', sa.Column('product_line', postgresql.ENUM('Standard', 'Touring', 'Road', 'Mountain', name='product_line'), autoincrement=False, nullable=True))
    op.add_column('transaction_n3', sa.Column('list_price', sa.NUMERIC(), autoincrement=False, nullable=False))
    op.add_column('transaction_n3', sa.Column('product_size', postgresql.ENUM('medium', 'large', 'small', name='product_size'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###