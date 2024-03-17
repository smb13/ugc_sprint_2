"""Генерация тестовых данных"""

import datetime as dt
import itertools
import logging
import random
import uuid
from collections.abc import Generator, Iterable
from contextlib import closing

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection, cursor
from psycopg2.extras import LoggingConnection, execute_batch

from core.common import log_time
from core.config import postgres_settings

logger = logging.getLogger(__name__)

DSN = (
    f"postgresql://{postgres_settings.user}:{postgres_settings.password}"
    f"@{postgres_settings.host}:{postgres_settings.port}/{postgres_settings.db}"
)


def create_db_and_tables(conn: connection) -> None:
    """Create database and tables.

    * Likes (user_id: uuid, film_id: uuid, rating: smallint, dt_created: timestamp);
    * Bookmarks (user_id: uuid, film_id: uuid, dt_created: timestamp);
    """

    with conn.cursor() as cur:
        cur: cursor

        logging.info("Drop tables 'likes' and 'bookmarks' if exists")
        cur.execute(
            """
            DROP TABLE IF EXISTS likes;
            DROP TABLE IF EXISTS bookmarks;
            """,
        )

        logging.info("Create tables 'likes' and 'bookmarks' if not exists")
        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS likes (
            user_id UUID,
            film_id UUID,
            rating SMALLINT,
            dt_created TIMESTAMP,
            PRIMARY KEY (user_id, film_id)
        );

        CREATE TABLE IF NOT EXISTS bookmarks (
            user_id UUID,
            film_id UUID,
            dt_created TIMESTAMP,
            PRIMARY KEY (user_id, film_id)
        );
        """,
        )

        logging.info("Create index likes(film_id) if not exists")
        cur.execute(
            """
            CREATE INDEX IF NOT EXISTS likes_film_id_idx ON likes(film_id);
            """,
        )

        logging.info("DB creation finished")


def data_generator(
    user_ids: Iterable[uuid.UUID],
    film_ids: list[uuid.UUID],
    amount_by_user: tuple[int, int],
) -> Generator[tuple[str, str, int, dt.datetime], None, None]:
    """Generates tuples of (user_id, film_id, rating, dt_created)"""
    scores = itertools.cycle(range(1, 11))

    for user_id in user_ids:
        films_amount = random.randint(*amount_by_user)
        for _ in range(films_amount):
            dt_created = dt.datetime.now().replace(
                year=random.randint(2010, 2020),
                month=random.randint(1, 12),
                day=random.randint(1, 28),
            )
            yield str(user_id), str(random.choice(film_ids)), next(scores), dt_created


def save_data_to_postgres(
    conn: "connection",
    table_name: str,
    column_names: Iterable[str],
    table_data: Iterable[tuple],
    batch_size: int,
) -> None:
    statement = sql.SQL(
        """
        INSERT INTO {table_name} ({column_names})
        VALUES ({row_placeholders})
        ON CONFLICT (user_id, film_id) DO NOTHING;
        """,
    ).format(
        table_name=sql.Identifier(table_name),
        column_names=sql.SQL(", ").join(map(sql.Identifier, column_names)),
        row_placeholders=sql.SQL(", ").join(sql.Placeholder() * len(column_names)),
    )

    for data_batch in itertools.batched(table_data, batch_size):
        with conn.cursor() as cur:
            execute_batch(
                cur,
                statement,
                data_batch,
                page_size=10000,
            )


def generate_test_data(
    conn: connection,
    users_amount: int = 100000,
    films_amount: int = 1000,
    batch_size: int = 10000,
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
    save_data_to_postgres(
        conn=conn,
        table_name="likes",
        column_names=("user_id", "film_id", "rating", "dt_created"),
        table_data=likes,
        batch_size=batch_size,
    )

    user_ids = (uuid.uuid4() for _ in range(users_amount))
    bookmarks = data_generator(user_ids, film_ids, bookmarks_per_user)
    save_data_to_postgres(
        conn=conn,
        table_name="bookmarks",
        column_names=("user_id", "film_id", "dt_created"),
        table_data=((u, f, d) for u, f, _, d in bookmarks),
        batch_size=batch_size,
    )


def main() -> None:
    with closing(psycopg2.connect(DSN, connection_factory=LoggingConnection)) as conn:
        conn: LoggingConnection
        conn.initialize(logger)
        conn.autocommit = True

        # Создание таблиц
        create_db_and_tables(conn)

        # Генерация тестовых данных
        users = 1_000_000
        with log_time("Postgres generates test data inserting", users * 10 + users * 10):
            generate_test_data(
                conn,
                users_amount=users,
                films_amount=10_000,
                batch_size=100_000,
                likes_per_user=(0, 20),
                bookmarks_per_user=(0, 20),
            )


if __name__ == "__main__":
    main()
