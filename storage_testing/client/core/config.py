import logging

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

console_out = logging.StreamHandler()
logging.basicConfig(handlers=(console_out,), level=logging.INFO)

# Класс настройки датасета


class DatasetSettings(BaseSettings):
    size: int = Field(100000)
    batch_size: int = Field(10000)


# Класс настройки MongoDB
class MongoSettings(BaseSettings):
    host: str = Field("mongo")
    port: int = Field(27017)

    model_config = SettingsConfigDict(env_prefix="mongo_", env_file=".env")


# Класс настройки PostgreSQL
class PostgresSettings(BaseSettings):
    host: str = Field("postgres")
    port: int = Field(5432)
    user: str
    password: str
    db: str = Field("ugc")

    model_config = SettingsConfigDict(env_prefix="postgres_", env_file=".env")


mongo_settings = MongoSettings()
postgres_settings = PostgresSettings()
dataset_settings = DatasetSettings()
