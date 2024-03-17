import datetime as dt
import logging
import random
import uuid

from mongo.common import mongo_client_context
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from core.common import log_time
from core.config import mongo_settings

logger = logging.getLogger(__name__)


def get_user_ids(mongo_db: Database, users_amount: int) -> list[int]:
    pipeline = [
        {"$group": {"_id": "$user_id"}},
        {"$limit": users_amount},
    ]

    return [u["_id"] for u in mongo_db.likes.aggregate(pipeline)]


def get_film_ids(mongo_db: Database, films_amount: int) -> list[int]:
    pipeline = [
        {"$group": {"_id": "$film_id"}},
        {"$limit": films_amount},
    ]

    return [f["_id"] for f in mongo_db.likes.aggregate(pipeline)]


def fetch_users_likes(mongo_db: Database, user_ids: list[int]) -> None:
    """Списки понравившихся пользователям фильмов (списки лайков пользователей)."""
    likes_collection = mongo_db.likes

    for user_id in user_ids:
        list(likes_collection.find({"user_id": user_id}))


def insert_user_like(mongo_db: Database, user_ids: list[int]) -> None:
    """Добавление оценки пользователя"""
    film_id = str(uuid.uuid4())
    likes_collection: Collection = mongo_db.likes

    for user_id in user_ids:
        likes_collection.insert_one(
            {"user_id": user_id, "film_id": film_id, "rating": random.randint(1, 10), "dt_created": dt.datetime.now()},
        )


def insert_and_fetch_user_like(mongo_db: Database, user_ids: list[int]) -> None:
    """Добавление оценки пользователя и получение оценок этого пользователя"""
    film_id = str(uuid.uuid4())
    likes_collection: Collection = mongo_db.likes

    for user_id in user_ids:
        likes_collection.insert_one(
            {"user_id": user_id, "film_id": film_id, "rating": random.randint(1, 10), "dt_created": dt.datetime.now()},
        )
        list(likes_collection.find({"user_id": user_id}))


def fetch_film_ratings(mongo_db: Database, film_ids: list[int]) -> None:
    """Средняя пользовательская оценка фильма."""
    for film_id in film_ids:
        pipeline = [
            {"$match": {"film_id": film_id}},  # Filter to only include documents for the specified film_id
            {
                "$group": {
                    "_id": "$film_id",  # Group by film_id
                    "average_rating": {"$avg": "$rating"},  # Calculate the average rating
                },
            },
        ]
        list(mongo_db.likes.aggregate(pipeline))


def insert_likes_and_fetch_film_rating(mongo_db: Database, film_ids: list[int]) -> None:
    """Добавление оценки пользователя и получение оценок этого пользователя"""
    likes_collection: Collection = mongo_db.likes

    for film_id in film_ids:
        likes_collection.insert_one(
            {
                "user_id": str(uuid.uuid4()),
                "film_id": film_id,
                "rating": random.randint(1, 10),
                "dt_created": dt.datetime.now(),
            },
        )
        pipeline = [
            {"$match": {"film_id": film_id}},  # Filter to only include documents for the specified film_id
            {
                "$group": {
                    "_id": "$film_id",  # Group by film_id
                    "average_rating": {"$avg": "$rating"},  # Calculate the average rating
                },
            },
        ]
        list(mongo_db.likes.aggregate(pipeline))


def main() -> None:
    with mongo_client_context(host=mongo_settings.host, port=mongo_settings.port) as client:
        client: MongoClient
        mongo_db: Database = client["ugc"]

        users_amount = 10_000
        user_ids = get_user_ids(mongo_db, users_amount)

        # Списки понравившихся пользователям фильмов (списки лайков пользователей).
        with log_time("Mongo returns likes for users", len(user_ids)):
            fetch_users_likes(mongo_db, user_ids)

        films_amount = 10_000
        film_ids = get_film_ids(mongo_db, films_amount)

        # Средняя пользовательская оценка фильма.
        with log_time("Mongo returns ratings for films", len(film_ids)):
            fetch_film_ratings(mongo_db, film_ids)

        # Тестирование единичной вставки
        # Добавление оценки пользователя
        with log_time("Mongo writes user like", len(user_ids)):
            insert_user_like(mongo_db, user_ids)

        # Тестирование чтения данных, поступающих в реальном времени
        # Добавление оценки пользователя и получение оценок этого пользователя
        with log_time("Mongo writes user like and returns it", len(user_ids)):
            insert_and_fetch_user_like(mongo_db, user_ids)

        # Добавление оценки пользователя и получение оценок этого пользователя
        film_ids = get_film_ids(mongo_db, int(films_amount / 10)) * 10
        with log_time("Mongo writes user like and returns films rating", len(film_ids)):
            insert_likes_and_fetch_film_rating(mongo_db, film_ids)


if __name__ == "__main__":
    main()
