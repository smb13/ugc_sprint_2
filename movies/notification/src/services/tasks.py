import datetime
import uuid
from functools import lru_cache
from http import HTTPStatus
from pprint import pprint

import bson
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException
from motor.core import AgnosticClient
from pymongo.errors import DuplicateKeyError

from core.config import settings
from db.mongo import get_mongo
from schemas.notifications import EmailNotification, PushNotificationState, PushNotification
from services.base import BaseService


class TasksService(BaseService):
    """
    Класс для реализации логики работы с задачами.
    """

    async def get_pushs(self, clients) -> list[PushNotification]:
        return []

    async def get_emails(self) -> list[EmailNotification]:
        mark=uuid.uuid4()
        a = await self.db_emails().update_many(
            {'$or': [
                {'updated_at': None},
                {'updated_at': {'$lt': datetime.datetime.utcnow() - datetime.timedelta(seconds=settings.send_timeout)}}
            ]},
            {'$set': {'updated_at': datetime.datetime.utcnow(), 'mark': str(mark)}}
        )
        if a.modified_count == 0:
            return []
        return [EmailNotification(**task) for task in
                await self.db_emails().find({'mark': str(mark)}).to_list(a.modified_count)]

    async def confirm(self, notifications) -> None:
        pass

#     async def send_email(self, request: EmailNotification):
#         try:
#             await self.db_emails().insert_one({
#                 "id": bson.Binary.from_uuid(request.id),
#                 "subject": request.subject,
#                 "to": request.to,
#                 "body": request.body,
#                 "delivered": False,
#                 "ts": datetime.datetime.utcnow()
#             })
#         except DuplicateKeyError:
#             raise HTTPException(
#                 status_code=HTTPStatus.CONFLICT, detail="Уведомление с таким идентификатором уже существует"
#             )
#
#     async def send_push(self, request):
#         try:
#             await self.db_pushs().insert_one({
#                 "id": bson.Binary.from_uuid(request.id),
#                 "subject": request.subject,
#                 "to": request.to,
#                 "body": request.body,
#                 "delivered": False,
#                 "read": False,
#                 "ts": datetime.datetime.utcnow()
#             })
#         except DuplicateKeyError:
#             raise HTTPException(
#                 status_code=HTTPStatus.CONFLICT, detail="Уведомление с таким идентификатором уже существует"
#             )
#
#     async def mark_as_read(self, notification_id):
#         await self.db_pushs().update_one({
#             'id': bson.Binary.from_uuid(notification_id)
#         }, {'$set': {'read': True}}, upsert=True)
#
#     async def list(self, user_id) -> list[PushNotificationState]:
#         return [PushNotificationState(**x, to=user_id) for x in
#                 await self.db_pushs().find(
#                     {"to": user_id, "delivered": True}, projection={"to": False}
#                 ).to_list(settings.push_limit)]


@lru_cache
def get_tasks_service(
    jwt: AuthJWT = Depends(),
    mongo: AgnosticClient = Depends(get_mongo),
) -> TasksService:
    return TasksService(jwt, mongo)
