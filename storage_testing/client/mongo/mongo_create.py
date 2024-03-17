"""Генерация тестовых данных"""

import itertools
import uuid
from collections.abc import Iterable

from mongo.common import mongo_client_context
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from core.common import data_generator, log_time
from core.config import mongo_settings


def save_data_to_mongo(
    db: Database,
    table_name: str,
    column_names: Iterable[str],
    table_data: Iterable[tuple],
    batch_size: int,
) -> None:
    collection: Collection = db[table_name]

    data_dict = (dict(zip(column_names, data)) for data in table_data)

    for data_batch in itertools.batched(data_dict, batch_size):
        collection.insert_many(data_batch)


def generate_test_data(
    mongo_db: Database,
    users_amount: int = 100_000,
    films_amount: int = 1000,
    batch_size: int = 10_000,
    likes_per_user: tuple[int, int] = (0, 50),
    bookmarks_per_user: tuple[int, int] = (0, 20),
) -> None:
    """Generate test data.

    * Likes (user_id: uuid, film_id: uuid, rating: smallint, dt_created: timestamp);
    * Bookmarks (user_id: uuid, film_id: uuid, dt_created: timestamp);
    """
    film_ids = [uuid.uuid4() for _ in range(films_amount)]

    user_ids = (uuid.uuid4() for _ in range(users_amount))
    likes = data_generator(user_ids, film_ids, likes_per_user)
    save_data_to_mongo(
        db=mongo_db,
        table_name="likes",
        column_names=("user_id", "film_id", "rating", "dt_created"),
        table_data=likes,
        batch_size=batch_size,
    )

    user_ids = (uuid.uuid4() for _ in range(users_amount))
    bookmarks = data_generator(user_ids, film_ids, bookmarks_per_user)
    save_data_to_mongo(
        db=mongo_db,
        table_name="bookmarks",
        column_names=("user_id", "film_id", "dt_created"),
        table_data=((u, f, d) for u, f, _, d in bookmarks),
        batch_size=batch_size,
    )


def main() -> None:
    with mongo_client_context(host=mongo_settings.host, port=mongo_settings.port) as client:
        client: MongoClient
        mongo_db: Database = client["ugc"]

        mongo_db.drop_collection("likes")
        mongo_db.drop_collection("bookmarks")

        mongo_db.likes.create_index("user_id")
        mongo_db.likes.create_index("film_id")
        mongo_db.likes.create_index(["user_id", "film_id"], unique=True)

        # Генерация тестовых данных
        users = 1_000_000
        with log_time("Mongo generates test data inserting", users * 10 + users * 10):
            generate_test_data(
                mongo_db,
                users_amount=users,
                films_amount=10_000,
                batch_size=100_000,
                likes_per_user=(0, 20),
                bookmarks_per_user=(0, 20),
            )


if __name__ == "__main__":
    main()
