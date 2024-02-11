import sqlalchemy
from sqlalchemy import Enum

metadata = sqlalchemy.MetaData()


order_status = Enum(
    "Approved",
    "Cancelled",
    name="order_status"
)

product_line = Enum(
    "Standard",
    "Touring",
    "Road",
    "Mountain",
    name="product_line"
)


product_class = Enum(
    "medium",
    "high",
    "low",
    name="product_class",
)


product_size = Enum(
    "medium",
    "large",
    "small",
    name="product_size",
)

gender = Enum(
    "Male",
    "Female",
    name="gender",
)

wealth_segment = Enum(
    "Affluent Customer",
    "High Net Worth",
    "Mass Customer",
    name="wealth_segment",
)

deceased_indicator = Enum(
    "N",
    "Y",
    name="deceased_indicator",
)

owns_car = Enum(
    "Yes",
    "No",
    name="owns_car",
)


customer = sqlalchemy.Table(
    "customer",
    metadata,
    sqlalchemy.Column("customer_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("gender", gender, nullable=False),
    sqlalchemy.Column("DOB", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("job_title", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("job_industry_category", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("wealth_segment", wealth_segment, nullable=False),
    sqlalchemy.Column("deceased_indicator", deceased_indicator, nullable=False),
    sqlalchemy.Column("owns_car", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("address", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("postcode", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("state", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("country", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("property_valuation", sqlalchemy.Integer, nullable=False),
)


transaction = sqlalchemy.Table(
    "transaction",
    metadata,
    sqlalchemy.Column("transaction_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("customer_id", sqlalchemy.Integer,  sqlalchemy.ForeignKey("customer.customer_id"), nullable=False),
    sqlalchemy.Column("transaction_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("online_order", sqlalchemy.Boolean, nullable=True),
    sqlalchemy.Column("order_status", order_status, nullable=False),
    sqlalchemy.Column("brand", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("product_line", product_line, nullable=True),
    sqlalchemy.Column("product_class", product_class, nullable=True),
    sqlalchemy.Column("product_size", product_size, nullable=True),
    sqlalchemy.Column("list_price", sqlalchemy.DECIMAL, nullable=False),
    sqlalchemy.Column("standard_cost", sqlalchemy.DECIMAL, nullable=True),
)


address = sqlalchemy.Table(
    "address",
    metadata,
    sqlalchemy.Column("address_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("address", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("postcode", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("state", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("country", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("property_valuation", sqlalchemy.Integer, nullable=False),
)


product = sqlalchemy.Table(
    "product",
    metadata,
    sqlalchemy.Column("product_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("brand", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("product_line", product_line, nullable=False),
    sqlalchemy.Column("product_class", product_class, nullable=False),
    sqlalchemy.Column("product_size", product_size, nullable=False),
    sqlalchemy.Column("list_price", sqlalchemy.DECIMAL, nullable=False),
    sqlalchemy.Column("standard_cost", sqlalchemy.DECIMAL, nullable=True),
)


customer_n3 = sqlalchemy.Table(
    "customer_n3",
    metadata,
    sqlalchemy.Column("customer_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("first_name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("gender", gender, nullable=False),
    sqlalchemy.Column("DOB", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("job_title", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("job_industry_category", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("wealth_segment", wealth_segment, nullable=False),
    sqlalchemy.Column("deceased_indicator", deceased_indicator, nullable=False),
    sqlalchemy.Column("owns_car", owns_car, nullable=False),
    sqlalchemy.Column("address_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("address.address_id"), nullable=False),
)


transaction_n3 = sqlalchemy.Table(
    "transaction_n3",
    metadata,
    sqlalchemy.Column("transaction_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("product.product_id"), nullable=False),
    sqlalchemy.Column("customer_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("customer_n3.customer_id"), nullable=False),
    sqlalchemy.Column("transaction_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("online_order", sqlalchemy.Boolean, nullable=True),
    sqlalchemy.Column("order_status", order_status, nullable=False),
)
