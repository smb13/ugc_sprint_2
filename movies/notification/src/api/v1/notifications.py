import uuid
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, Body
from fastapi.security import HTTPBearer

from core.config import settings
from schemas.notifications import EmailNotification, PushNotification

router = APIRouter(redirect_slashes=False)


@router.post(
    path="/email",
    summary="Отправка email нотификации",
    status_code=HTTPStatus.CREATED,
)
async def send(
    request: EmailNotification = Body(...)
) -> None:
    # await bookmarks_service.add(movie_id)
    pass

@router.post(
    path="/push",
    summary="Отправка push нотификации",
    status_code=HTTPStatus.CREATED,
)
async def send(
    request: PushNotification = Body(...)
) -> None:
    # await bookmarks_service.add(movie_id)
    pass


@router.post(
    path="/push/{notification_id}",
    summary="Отметка уведомления как прочитанного",
    status_code=HTTPStatus.CREATED,
)
async def read() -> list[PushNotification]:
    # await bookmarks_service.add(movie_id)
    pass


@router.get(
    path="/push/{user_id}",
    summary="Получение списка доставленных push уведомлений",
    status_code=HTTPStatus.CREATED,
)
async def history() -> list[PushNotification]:
    # await bookmarks_service.add(movie_id)
    pass