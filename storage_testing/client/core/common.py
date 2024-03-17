import logging
import time as tm
from collections.abc import Generator
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
