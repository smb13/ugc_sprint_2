import datetime as dt
import itertools
import logging
import random
import time as tm
import uuid
from collections.abc import Generator, Iterable
from contextlib import contextmanager

from tqdm import tqdm

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

    # Ensure that max amount of films per user not exceeds amount of films
    amount_by_user = (min(amount_by_user[0], len(film_ids)), min(amount_by_user[1], len(film_ids)))

    for user_id in tqdm(user_ids):
        films_amount = random.randint(*amount_by_user)
        for film_id in random.sample(film_ids, films_amount):
            dt_created = dt.datetime.now().replace(
                year=random.randint(2010, 2020),
                month=random.randint(1, 12),
                day=random.randint(1, 28),
            )
            yield str(user_id), str(film_id), next(scores), dt_created
