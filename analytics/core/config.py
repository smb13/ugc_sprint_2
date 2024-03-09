from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class ProjectSettings(BaseSettings):
    name: str = Field("Analytics Service")
    authjwt_secret_key: str
    authjwt_algorithm: str = "HS256"

    model_config = SettingsConfigDict(env_prefix="project_", env_file=".env", extra="ignore")


# Класс настройки Kafka
class KafkaSettings(BaseSettings):
    connection_string: str = Field("localhost:9094")

    model_config = SettingsConfigDict(env_prefix="kafka_", env_file=".env", extra="ignore")


class GunicornSettings(BaseSettings):
    host: str = Field("0.0.0.0")
    port: int = Field(8000)
    workers: int = Field(2)
    loglevel: str = Field("debug")
    model_config = SettingsConfigDict(env_prefix="gunicorn_", env_file=".env")


gunicorn_settings = GunicornSettings()
project_settings = ProjectSettings()
kafka_settings = KafkaSettings()
