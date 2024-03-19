import logging
import random
import uuid
from contextlib import closing

import psycopg2
from psycopg2.extensions import connection, cursor
from psycopg2.extras import LoggingConnection

from core.common import log_time
from core.config import postgres_settings

logger = logging.getLogger(__name__)

DSN = (
    f"postgresql://{postgres_settings.user}:{postgres_settings.password}"
    f"@{postgres_settings.host}:{postgres_settings.port}/{postgres_settings.db}"
)


def get_user_ids(conn: connection, users_amount: int) -> list[int]:
    with conn.cursor() as cur:
        cur: cursor

        cur.execute(
            """
            SELECT DISTINCT user_id FROM likes LIMIT %s;
            """,
            (users_amount,),
        )
        rows = cur.fetchall()

    return [u[0] for u in rows]


def get_film_ids(conn: connection, films_amount: int) -> list[int]:
    with conn.cursor() as cur:
        cur: cursor

        cur.execute(
            """
            SELECT DISTINCT film_id FROM likes LIMIT %s;
            """,
            (films_amount,),
        )
        rows = cur.fetchall()

    return [u[0] for u in rows]


def fetch_users_likes(conn: connection, user_ids: list[int]) -> None:
    """Списки понравившихся пользователям фильмов (списки лайков пользователей)."""
    with conn.cursor() as cur:
        cur: cursor

        for user_id in user_ids:
            cur.execute(
                """
                SELECT * FROM likes WHERE user_id = %s;
                """,
                (user_id,),
            )
            cur.fetchall()


def insert_user_like(conn: connection, user_ids: list[int]) -> None:
    """Добавление оценки пользователя"""
    film_id = str(uuid.uuid4())

    for user_id in user_ids:
        with conn.cursor() as cur:
            cur: cursor

            cur.execute(
                """
                INSERT INTO likes VALUES (%s, %s, %s, now());
                """,
                (user_id, film_id, random.randint(1, 10)),
            )


def insert_and_fetch_user_like(conn: connection, user_ids: list[int]) -> None:
    """Добавление оценки пользователя и получение оценок этого пользователя"""
    film_id = str(uuid.uuid4())

    for user_id in user_ids:
        with conn.cursor() as cur:
            cur: cursor

            cur.execute(
                """
                INSERT INTO likes VALUES (%s, %s, %s, now());
                """,
                (user_id, film_id, random.randint(1, 10)),
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT * FROM likes WHERE user_id = %s;
                """,
                (user_id,),
            )
            cur.fetchall()


def fetch_film_ratings(conn: connection, film_ids: list[int]) -> None:
    """Средняя пользовательская оценка фильма."""
    with conn.cursor() as cur:
        for film_id in film_ids:
            cur.execute(
                """
                SELECT AVG(rating) FROM likes WHERE film_id = %s;
                """,
                (film_id,),
            )
            cur.fetchone()


def insert_likes_and_fetch_film_rating(conn: connection, film_ids: list[int]) -> None:
    """Добавление оценки пользователя и получение оценок этого пользователя"""
    for film_id in film_ids:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO likes VALUES (%s, %s, %s, now());
                """,
                (str(uuid.uuid4()), film_id, random.randint(1, 10)),
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(rating) FROM likes WHERE film_id = %s;
                """,
                (film_id,),
            )
            cur.fetchone()


def main() -> None:
    with closing(psycopg2.connect(DSN, connection_factory=LoggingConnection)) as conn:
        conn: LoggingConnection
        conn.initialize(logger)
        conn.autocommit = True

        users_amount = 10_000
        user_ids = get_user_ids(conn, users_amount)

        # Списки понравившихся пользователям фильмов (списки лайков пользователей)
        with log_time("Postgres returns likes for users", len(user_ids)):
            fetch_users_likes(conn, user_ids)

        films_amount = 10_000
        film_ids = get_film_ids(conn, films_amount)

        # Средняя пользовательская оценка фильма
        with log_time("Postgres returns ratings for films", len(film_ids)):
            fetch_film_ratings(conn, film_ids)

        # Тестирование единичной вставки
        # Добавление оценки пользователя
        with log_time("Postgres writes user like", len(user_ids)):
            insert_user_like(conn, user_ids)

        # Тестирование чтения данных, поступающих в реальном времени
        # Добавление оценки пользователя и получение оценок этого пользователя
        with log_time("Postgres writes user like and returns it", len(user_ids)):
            insert_and_fetch_user_like(conn, user_ids)

        # Добавление оценки к фильму и получение средней пользовательской оценки этого фильма
        film_ids = get_film_ids(conn, int(films_amount / 10)) * 10
        with log_time("Postgres writes user like and returns films rating", len(film_ids)):
            insert_likes_and_fetch_film_rating(conn, film_ids)


if __name__ == "__main__":
    main()
