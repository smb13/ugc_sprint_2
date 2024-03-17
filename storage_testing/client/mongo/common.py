from collections.abc import Generator
from contextlib import contextmanager

from pymongo import MongoClient


@contextmanager
def mongo_client_context(*args, **kwargs) -> Generator[MongoClient, None, None]:
    client = MongoClient(*args, **kwargs)
    try:
        yield client
    finally:
        client.close()
