from typing import Literal

import pandas as pd
from loguru import logger
from pydantic import TypeAdapter
from sqlalchemy import create_engine

from src.config import ProjectConfig
from src.models import (Address, DenormalizedCustomer, DenormalizedTransaction,
                        NormalizedN3Customer, NormalizedN3Transaction, Product)
from src.repositories import (AddressRepository,
                              DenormalizedCustomerRepository,
                              DenormalizedTransactionRepository,
                              NormalizedN3CustomerRepository,
                              NormalizedN3TransactionRepository,
                              ProductRepository)


class DenormalizedETL:

    _conf = ProjectConfig()

    def __init__(self):
        logger.info("Инициализация DenormalizedETL...")
        engine = create_engine(str(self._conf.postgres_dsn))
        self._repo_customer = DenormalizedCustomerRepository(engine)
        self._repo_transaction = DenormalizedTransactionRepository(engine)

    def extract_data(self, sheet_name: Literal["customer", "transaction"]) -> pd.DataFrame:
        logger.info(f"Извлечение данных из листа {sheet_name}...")
        df = pd.read_excel(self._conf.source_data_path, sheet_name=sheet_name)
        df.fillna("", inplace=True)
        return df

    @classmethod
    def transform_data(
        cls,
        data: pd.DataFrame,
        obj: type[DenormalizedCustomer] | type[DenormalizedTransaction],
    ) -> tuple[DenormalizedCustomer | DenormalizedTransaction]:
        logger.info(f"Преобразование данных в объекты {obj.__name__}...")
        return TypeAdapter(tuple[obj, ...]).validate_python(data.to_dict(orient="records"))

    def load_data(
        self,
        data: tuple[DenormalizedCustomer | DenormalizedTransaction],
        type_: Literal["customer", "transaction"],
    ) -> None:
        logger.info(f"Загрузка данных в базу данных...")
        if type_ == "customer":
            logger.info(f"Загрузка данных в таблицу {type_}...")
            self._repo_customer.insert_many(data)
        elif type_ == "transaction":
            logger.info(f"Загрузка данных в таблицу {type_}...")
            self._repo_transaction.insert_many(data)

    def run(self) -> None:
        customer_data = self.extract_data("customer")
        customer_cast_rows = self.transform_data(customer_data, DenormalizedCustomer)

        transaction_data = self.extract_data("transaction")
        transaction_cast_rows = self.transform_data(transaction_data, DenormalizedTransaction)
        customer_ids = frozenset(row.customer_id for row in customer_cast_rows)

        valid_transaction_cast_rows = tuple(
            row
            for row in transaction_cast_rows
            if row.customer_id in customer_ids
        )
        self.load_data(customer_cast_rows, "customer")
        self.load_data(valid_transaction_cast_rows, "transaction")


class NormalizedN3ETL:
    _conf = ProjectConfig()

    def __init__(self):
        logger.info("Инициализация NormalizedN3ETL...")
        engine = create_engine(str(self._conf.postgres_dsn))
        self._repo_customer = NormalizedN3CustomerRepository(engine)
        self._repo_transaction = NormalizedN3TransactionRepository(engine)
        self._repo_address = AddressRepository(engine)
        self._repo_product = ProductRepository(engine)

    def extract_data(self, sheet_name: Literal["customer", "transaction"]) -> pd.DataFrame:
        logger.info(f"Извлечение данных из листа {sheet_name}...")
        df = pd.read_excel(self._conf.source_data_path, sheet_name=sheet_name)
        df.fillna("", inplace=True)
        return df

    @classmethod
    def transform_data(
        cls,
        data: pd.DataFrame,
        obj: type[Address] | type[Product] | type[NormalizedN3Customer] | type[NormalizedN3Transaction],
    ) -> tuple[Address | Product | NormalizedN3Customer | NormalizedN3Transaction]:
        logger.info(f"Преобразование данных в объекты {obj.__name__}...")
        return TypeAdapter(tuple[obj, ...]).validate_python(data.to_dict(orient="records"))

    def load_data(
        self,
        data: tuple[Address | Product | NormalizedN3Customer | NormalizedN3Transaction],
        type_: Literal["address", "product", "customer", "transaction"],
    ) -> None:
        logger.info(f"Загрузка данных в базу данных...")
        if type_ == "address":
            logger.info(f"Загрузка данных в таблицу {type_}...")
            self._repo_address.insert_many(data)
        elif type_ == "product":
            logger.info(f"Загрузка данных в таблицу {type_}...")
            self._repo_product.insert_many(data)
        elif type_ == "customer":
            logger.info(f"Загрузка данных в таблицу {type_}...")
            self._repo_customer.insert_many(data)
        elif type_ == "transaction":
            logger.info(f"Загрузка данных в таблицу {type_}...")
            self._repo_transaction.insert_many(data)

    def run(self) -> None:
        transaction_data = self.extract_data("transaction")
        transaction_cast_rows = self.transform_data(transaction_data, NormalizedN3Transaction)
        product_cast_row = self.transform_data(transaction_data, Product)
        product_cast_row: tuple[Product] = tuple(frozenset(product_cast_row))

        customer_data = self.extract_data("customer")
        customer_data["address_id"] = customer_data[["address", "country"]].sum(axis=1).map(
            lambda el: abs(hash(el)) % len(customer_data),
        )

        customer_cast_rows = self.transform_data(customer_data, NormalizedN3Customer)
        address_cast_rows = self.transform_data(customer_data, Address)
        address_cast_rows: tuple[Address] = tuple(frozenset(address_cast_rows))

        customer_ids = frozenset(row.customer_id for row in customer_cast_rows)
        product_ids = frozenset(row.product_id for row in product_cast_row)

        transaction_cast_rows = tuple(
            row
            for row in transaction_cast_rows
            if row.customer_id in customer_ids and row.product_id in product_ids
        )

        self.load_data(address_cast_rows, "address")
        self.load_data(product_cast_row, "product")
        self.load_data(customer_cast_rows, "customer")
        self.load_data(transaction_cast_rows, "transaction")


def main() -> None:
    DenormalizedETL().run()
    NormalizedN3ETL().run()


if __name__ == "__main__":
    main()
