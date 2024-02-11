from pydantic import BaseModel
from sqlalchemy import Engine

from src.tables import address
from src.tables import customer as denormalized_customer
from src.tables import customer_n3 as normalized_customer
from src.tables import product
from src.tables import transaction as denormalized_transaction
from src.tables import transaction_n3 as normalized_transaction


class BaseRepository:

    _table = None

    def __init__(self, engine: Engine):
        self.engine = engine

    def insert_many(self, rows: tuple[BaseModel]) -> None:
        with self.engine.connect() as conn:
            conn.execute(self._table.insert(), [row.dict(by_alias=True) for row in rows])
            conn.commit()


class DenormalizedCustomerRepository(BaseRepository):
    _table = denormalized_customer


class DenormalizedTransactionRepository(BaseRepository):
    _table = denormalized_transaction


class NormalizedN3CustomerRepository(BaseRepository):
    _table = normalized_customer


class NormalizedN3TransactionRepository(BaseRepository):
    _table = normalized_transaction


class AddressRepository(BaseRepository):
    _table = address


class ProductRepository(BaseRepository):
    _table = product
