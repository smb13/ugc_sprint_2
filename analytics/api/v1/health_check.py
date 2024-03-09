from http import HTTPStatus

from fastapi import APIRouter, Depends, Path

from schemas.error import HttpExceptionModel
from schemas.event import CreateEventResponse, HealthCheckResponse

router = APIRouter(redirect_slashes=False, prefix="", tags=["Health check"])


@router.get(
    "",
    summary="Проверка состояния работы сервиса",
    response_model=HealthCheckResponse,
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.BAD_REQUEST: {"model": HttpExceptionModel},
        HTTPStatus.UNAUTHORIZED: {"model": HttpExceptionModel},
        HTTPStatus.FORBIDDEN: {"model": HttpExceptionModel},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": HttpExceptionModel},
    },
)
async def health_check() -> CreateEventResponse:
    return {"status": "ok"}
