from async_fastapi_jwt_auth import AuthJWT
from pymongo import MongoClient

from core.config import settings


class BaseService:
    """
    Базовый класс для работы с бизнес-логикой
    """

    def __init__(self, jwt: AuthJWT, mongo: MongoClient) -> None:
        self.jwt = jwt
        self.mongo = mongo

    def db(self):
        return self.mongo[settings.mongo_db][settings.mongo_rating_collection]
