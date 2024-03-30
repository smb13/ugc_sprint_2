from async_fastapi_jwt_auth import AuthJWT
from motor.core import AgnosticClient

from core.config import settings


class BaseService:
    """
    Базовый класс для работы с бизнес-логикой
    """

    def __init__(self, jwt: AuthJWT, mongo: AgnosticClient) -> None:
        self.jwt = jwt
        self.mongo = mongo

    def db(self):
        return self.mongo[settings.mongo_db]

    def db_pushs(self):
        return self.db()[settings.mongo_pushs_collection]

    def db_emails(self):
        return self.db()[settings.mongo_emails_collection]
