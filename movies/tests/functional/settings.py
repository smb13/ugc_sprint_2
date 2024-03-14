from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    # Настройки Redis
    redis_host: str = "redis"
    redis_port: int = 6379

    # Настройки Elasticsearch
    elastic_host: str = "elastic"
    elastic_port: int = 9200

    # Должно соответствовать URL приложения в контейнере
    service_url: str = "http://external_dev:8000"

    # Настройки приложения
    page_size: int = 10
    page_size_max: int = 100


test_settings = TestSettings()
