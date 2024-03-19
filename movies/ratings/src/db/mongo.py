from pymongo import MongoClient
mongo: MongoClient | None = None


def connect(dsn):
    global mongo
    if mongo:
        mongo.close()

    mongo = MongoClient(dsn)

    return mongo


async def get_mongo() -> MongoClient:
    return mongo
