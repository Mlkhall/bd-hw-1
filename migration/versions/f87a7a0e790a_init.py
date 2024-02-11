"""init

Revision ID: f87a7a0e790a
Revises: 
Create Date: 2024-02-11 18:37:20.447017

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f87a7a0e790a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('postcode', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('property_valuation', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('address_id')
    )
    op.create_table('customer',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('gender', sa.Enum('Male', 'Female', name='gender'), nullable=False),
    sa.Column('DOB', sa.DateTime(), nullable=True),
    sa.Column('job_title', sa.String(), nullable=True),
    sa.Column('job_industry_category', sa.String(), nullable=True),
    sa.Column('wealth_segment', sa.Enum('Affluent Customer', 'High Net Worth', 'Mass Customer', name='wealth_segment'), nullable=False),
    sa.Column('deceased_indicator', sa.Enum('N', 'Y', name='deceased_indicator'), nullable=False),
    sa.Column('owns_car', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=False),
    sa.Column('postcode', sa.Integer(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('property_valuation', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('product_line', sa.Enum('Standard', 'Touring', 'Road', 'Mountain', name='product_line'), nullable=False),
    sa.Column('product_class', sa.Enum('medium', 'high', 'low', name='product_class'), nullable=False),
    sa.Column('product_size', sa.Enum('medium', 'large', 'small', name='product_size'), nullable=False),
    sa.Column('list_price', sa.DECIMAL(), nullable=False),
    sa.Column('standard_cost', sa.DECIMAL(), nullable=True),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_table('customer_n3',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('gender', sa.Enum('Male', 'Female', name='gender'), nullable=False),
    sa.Column('DOB', sa.DateTime(), nullable=True),
    sa.Column('job_title', sa.String(), nullable=True),
    sa.Column('job_industry_category', sa.String(), nullable=True),
    sa.Column('wealth_segment', sa.Enum('Affluent Customer', 'High Net Worth', 'Mass Customer', name='wealth_segment'), nullable=False),
    sa.Column('deceased_indicator', sa.Enum('N', 'Y', name='deceased_indicator'), nullable=False),
    sa.Column('owns_car', sa.Enum('Yes', 'No', name='owns_car'), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['address.address_id'], ),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('transaction',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('transaction_date', sa.DateTime(), nullable=False),
    sa.Column('online_order', sa.Boolean(), nullable=True),
    sa.Column('order_status', sa.Enum('Approved', 'Cancelled', name='order_status'), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('product_line', sa.Enum('Standard', 'Touring', 'Road', 'Mountain', name='product_line'), nullable=True),
    sa.Column('product_class', sa.Enum('medium', 'high', 'low', name='product_class'), nullable=True),
    sa.Column('product_size', sa.Enum('medium', 'large', 'small', name='product_size'), nullable=True),
    sa.Column('list_price', sa.DECIMAL(), nullable=False),
    sa.Column('standard_cost', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.customer_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    op.create_table('transaction_n3',
    sa.Column('transaction_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('transaction_date', sa.DateTime(), nullable=False),
    sa.Column('online_order', sa.Boolean(), nullable=True),
    sa.Column('order_status', sa.Enum('Approved', 'Cancelled', name='order_status'), nullable=False),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('product_line', sa.Enum('Standard', 'Touring', 'Road', 'Mountain', name='product_line'), nullable=True),
    sa.Column('product_class', sa.Enum('medium', 'high', 'low', name='product_class'), nullable=True),
    sa.Column('product_size', sa.Enum('medium', 'large', 'small', name='product_size'), nullable=True),
    sa.Column('list_price', sa.DECIMAL(), nullable=False),
    sa.Column('standard_cost', sa.DECIMAL(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customer_n3.customer_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.product_id'], ),
    sa.PrimaryKeyConstraint('transaction_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_n3')
    op.drop_table('transaction')
    op.drop_table('customer_n3')
    op.drop_table('product')
    op.drop_table('customer')
    op.drop_table('address')
    # ### end Alembic commands ###
