import uuid
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Body

from schemas.notifications import EmailNotification, PushNotification, PushNotificationState
from services.notifications import get_notifications_service, NotificationsService

router = APIRouter(redirect_slashes=False)


@router.post(
    path="/email",
    summary="Отправка email нотификации",
    status_code=HTTPStatus.CREATED,
)
async def send(
    request: EmailNotification = Body(...),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> None:
    await notifications_service.send_email(request)


@router.post(
    path="/push",
    summary="Отправка push нотификации",
    status_code=HTTPStatus.CREATED,
)
async def send(
    request: PushNotification = Body(...),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> None:
    await notifications_service.send_push(request)


@router.post(
    path="/push/{notification_id}",
    summary="Отметка уведомления как прочитанного",
    status_code=HTTPStatus.CREATED,
)
async def read(
    notification_id: UUID = Path(..., description="Идентификатор уведомления", example=uuid.uuid4()),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> None:
    await notifications_service.mark_as_read(notification_id)


@router.get(
    path="/push/{user_id}",
    summary="Получение списка доставленных push уведомлений",
    status_code=HTTPStatus.OK,
)
async def history(
    user_id: str = Path(..., description="Идентификатор пользователя", example="test@test.com"),
    notifications_service: NotificationsService = Depends(get_notifications_service),
) -> list[PushNotificationState]:
    return await notifications_service.list(user_id)
