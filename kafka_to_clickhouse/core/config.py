import os
from dataclasses import dataclass

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")


class ProjectSettings(BaseModel):
    base_path: str = BASE_DIR
    batch_size: int = Field(default=1000)
    backoff_max_tries: int = 30


class LogSettings(BaseSettings):
    # используем extra: ignore чтобы пропускать другие незаданные значения
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore")
    log_level: int = Field(default=30)
    log_format: str = "%(asctime)s [%(levelname).1s]: [in %(filename)s: line %(lineno)d] - %(message)s"


class ClickhouseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="clickhouse_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )
    host: str = ...
    port: int = Field(default=9000)
    database: str = Field(default="")
    user: str = Field(default="default")
    password: str = Field(default="")
    alt_hosts: str = ...


class KafkaSettings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_prefix="kafka_",
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
    )
    bootstrap_servers: str = Field(default="localhost:9094")
    request_timeout: int = Field(default=30)
    topic_subscribe: list[str] = Field(default=["user", "film"])


@dataclass
class Settings:
    logger: LogSettings = LogSettings()
    database: ClickhouseSettings = ClickhouseSettings()
    project: ProjectSettings = ProjectSettings()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
