import uuid
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Body

from schemas.notifications import EmailNotification, PushNotification

router = APIRouter(redirect_slashes=False)


@router.get(
    path="/email",
    summary="Получение email нотификации для отправки",
    status_code=HTTPStatus.CREATED,
)
async def get(
    # request: EmailNotification = Body(...)
) -> EmailNotification:
    # await bookmarks_service.add(movie_id)
    pass


@router.get(
    path="/push",
    summary="Получение push нотификаций для доставки клиенту",
    status_code=HTTPStatus.CREATED,
)
async def send(
    clients: list[str] = Body(..., description="Список доступных клиентов",
                              examples=[["test@test.com", "vasya@test.com"]])
) -> list[PushNotification]:
    # await bookmarks_service.add(movie_id)
    pass


@router.post(
    path="/confirm",
    summary="Подтверждение отправки нотификации клиенту",
    status_code=HTTPStatus.CREATED,
)
async def send(
    notifications: list[UUID] = Body(..., description="Список идентификаторов нотификаций",
                              examples=[[uuid.uuid4(), uuid.uuid4()]])
) -> list[PushNotification]:
    # await bookmarks_service.add(movie_id)
    pass
