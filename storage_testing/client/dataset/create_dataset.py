import random
import string


def generate_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_data_batch(batch_size: int) -> list:
    data = list()
    for _i in range(batch_size):
        name = generate_random_string(10)
        data.append((random.randint(0, 2**32), name, random.randint(0, 2**32)))
    return data
