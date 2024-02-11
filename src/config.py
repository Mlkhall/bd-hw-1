from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class _BaseConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file="local.env",
    )


class DBConfig(_BaseConfig):
    postgres_dsn: PostgresDsn


class ProjectConfig(DBConfig):
    source_data_path: Path = Path("customer_and_transaction.xlsx")
