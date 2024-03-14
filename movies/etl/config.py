from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_user: str = "etl"
    postgres_password: str
    postgres_movies_db: str = "movies_database"
    postgres_port: int = 5432

    elastic_port: int = 9200

    redis_port: int
    redis_states_db: int

    batch_size: int = 100


settings = Settings()
