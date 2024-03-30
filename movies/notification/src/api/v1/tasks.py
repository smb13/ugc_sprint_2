import uuid
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Body, Depends

from schemas.notifications import EmailNotification, PushNotification
from services.tasks import TasksService, get_tasks_service

router = APIRouter(redirect_slashes=False)


@router.get(
    path="/email",
    summary="Получение email нотификации для отправки",
    status_code=HTTPStatus.OK,
)
async def get(
    tasks_service: TasksService = Depends(get_tasks_service)
) -> list[EmailNotification]:
    return await tasks_service.get_emails()


@router.get(
    path="/push",
    summary="Получение push нотификаций для доставки клиенту",
    status_code=HTTPStatus.OK,
)
async def send(
    clients: list[str] = Body(..., description="Список доступных клиентов",
                              examples=[["test@test.com", "vasya@test.com"]]),
    tasks_service: TasksService = Depends(get_tasks_service)
) -> list[PushNotification]:
    return await tasks_service.get_pushs(clients)


@router.post(
    path="/confirm",
    summary="Подтверждение отправки нотификации клиенту",
    status_code=HTTPStatus.OK,
)
async def confirm(
    notifications: list[UUID] = Body(
        ..., description="Список идентификаторов нотификаций", examples=[[uuid.uuid4(), uuid.uuid4()]]),
    tasks_service: TasksService = Depends(get_tasks_service)
) -> None:
    return await tasks_service.confirm(notifications)
