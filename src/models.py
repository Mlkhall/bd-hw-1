from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import (BaseModel, Field, NonNegativeInt, PositiveInt,
                      field_validator)


class OrderStatus(StrEnum):
    approved = "Approved"
    cancelled = "Cancelled"


class ProductLine(StrEnum):
    standard = "Standard"
    touring = "Touring"
    road = "Road"
    mountain = "Mountain"


class ProductClass(StrEnum):
    medium = "medium"
    high = "high"
    low = "low"


class ProductSize(StrEnum):
    medium = "medium"
    large = "large"
    small = "small"


class Gender(StrEnum):
    male = "Male"
    female = "Female"


class WealthSegment(StrEnum):
    affluent_customer = "Affluent Customer"
    high_net_worth = "High Net Worth"
    mass_customer = "Mass Customer"


class DeceasedIndicator(StrEnum):
    no = "N"
    yes = "Y"


class OwnsCar(StrEnum):
    yes = "Yes"
    no = "No"


class DenormalizedCustomer(BaseModel):
    customer_id: NonNegativeInt
    first_name: str
    last_name: str | None
    gender: Gender | None
    date_of_birth: datetime | None = Field(alias="DOB")
    job_title: str | None
    job_industry_category: str | None
    wealth_segment: WealthSegment
    deceased_indicator: DeceasedIndicator
    owns_car: OwnsCar
    address: str
    postcode: PositiveInt
    state: str
    country: str
    property_valuation: PositiveInt

    @field_validator("gender", mode="before")
    @classmethod
    def _gender_must_be_valid(cls, gender: str) -> Gender:
        match gender:
            case Gender.male | "M" | "U":
                return Gender.male
            case Gender.female | "Female" | "F" | "Femal":
                return Gender.female
            case _:
                raise ValueError(f"Неизвестный пол: {gender}")

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def _date_of_birth_must_be_valid(cls, date_of_birth: str) -> str | None:
        if not date_of_birth:
            return
        return date_of_birth


class DenormalizedTransaction(BaseModel):
    transaction_id: NonNegativeInt
    product_id: NonNegativeInt
    customer_id: NonNegativeInt
    transaction_date: datetime
    online_order: bool | None
    order_status: OrderStatus
    brand: str | None
    product_line: ProductLine | None
    product_class: ProductClass | None
    product_size: ProductSize | None
    list_price: Decimal
    standard_cost: Decimal | None

    @field_validator("*", mode="before")
    @classmethod
    def _all_values_must_be_valid(cls, value: str | int) -> str | None:
        if not value and value != 0:
            return
        return value


class Address(BaseModel):
    address_id: NonNegativeInt
    address: str
    postcode: PositiveInt
    state: str
    country: str
    property_valuation: PositiveInt

    def __hash__(self):
        return self.address_id

    def __eq__(self, other):
        return self.address_id == other.address_id


class Product(BaseModel):
    product_id: NonNegativeInt
    brand: str | None
    product_line: ProductLine | None
    product_class: ProductClass | None
    product_size: ProductSize | None
    list_price: Decimal
    standard_cost: Decimal | None

    @field_validator("*", mode="before")
    @classmethod
    def _all_values_must_be_valid(cls, value: str | int) -> str | None:
        if not value and value != 0:
            return
        return value

    def __hash__(self):
        return self.product_id

    def __eq__(self, other):
        return self.product_id == other.product_id


class NormalizedN3Customer(BaseModel):
    customer_id: NonNegativeInt
    first_name: str
    last_name: str | None
    gender: Gender
    date_of_birth: datetime | None = Field(alias="DOB")
    job_title: str | None
    job_industry_category: str | None
    wealth_segment: WealthSegment
    deceased_indicator: DeceasedIndicator
    owns_car: OwnsCar
    address_id: NonNegativeInt

    @field_validator("gender", mode="before")
    @classmethod
    def _gender_must_be_valid(cls, gender: str) -> Gender:
        match gender:
            case Gender.male | "M" | "U":
                return Gender.male
            case Gender.female | "Female" | "F" | "Femal":
                return Gender.female
            case _:
                raise ValueError(f"Неизвестный пол: {gender}")

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def _date_of_birth_must_be_valid(cls, date_of_birth: str) -> str | None:
        if not date_of_birth:
            return
        return date_of_birth


class NormalizedN3Transaction(BaseModel):
    transaction_id: NonNegativeInt
    product_id: NonNegativeInt
    transaction_date: datetime
    customer_id: NonNegativeInt
    online_order: bool | None
    order_status: OrderStatus

    @field_validator("*", mode="before")
    @classmethod
    def _all_values_must_be_valid(cls, value: str | int) -> str | None:
        if not value and value != 0:
            return
        return value
