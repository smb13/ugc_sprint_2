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

    async def get_push_tasks(self, clients) -> list[PushNotification]:
        mark = uuid.uuid4()
        a = await self.db_pushs().update_many(
            {
                '$or': [
                    {'updated_at': None},
                    {'updated_at': {
                        '$lt': datetime.datetime.utcnow() - datetime.timedelta(seconds=settings.send_timeout)}}],
                'delivered_at': None},
            {'$set': {'updated_at': datetime.datetime.utcnow(), 'mark': str(mark)}}
        )
        if a.modified_count == 0:
            return []
        return [PushNotification(**task) for task in
                await self.db_pushs().find({'mark': str(mark)}).to_list(a.modified_count)]

    async def get_email_task(self) -> list[EmailNotification]:
        mark = uuid.uuid4()
        a = await self.db_emails().update_one(
            {
                '$or': [
                    {'updated_at': None},
                    {'updated_at': {
                        '$lt': datetime.datetime.utcnow() - datetime.timedelta(seconds=settings.send_timeout)}}],
                'delivered_at': None},
            {'$set': {'updated_at': datetime.datetime.utcnow(), 'mark': str(mark)}}
        )
        if a.modified_count == 0:
            return []
        return [EmailNotification(**task) for task in
                await self.db_emails().find({'mark': str(mark)}).to_list(a.modified_count)]

    async def confirm(self, notifications) -> None:
        await self.db_pushs().update_many(
            {'id': {'$in': [bson.Binary.from_uuid(notification_id) for notification_id in notifications]}},
            {'$set': {'delivered_at': datetime.datetime.utcnow()}},
            upsert=True
        )

@lru_cache
def get_tasks_service(
    jwt: AuthJWT = Depends(),
    mongo: AgnosticClient = Depends(get_mongo),
) -> TasksService:
    return TasksService(jwt, mongo)
