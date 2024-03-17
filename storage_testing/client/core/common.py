import datetime as dt
import itertools
import logging
import random
import time as tm
import uuid
from collections.abc import Generator, Iterable
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def log_time(task_name: str, size: int) -> Generator:
    try:
        start_time = tm.time()
        yield
    finally:
        elapsed_time = tm.time() - start_time
        logging.info(f"{task_name} {size} records in: {elapsed_time:.3f} s")


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
