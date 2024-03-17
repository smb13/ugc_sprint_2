import uuid
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query
from fastapi.security import HTTPBearer

from core.config import settings
from schemas.bookmarks import BookmarksListResponse
from services.bookmarks import BookmarksService, get_bookmark_service

router = APIRouter(redirect_slashes=False)


@router.post(
    path="/{movie_id}",
    summary="Добавление фильма в закладки",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(HTTPBearer())],
)
async def add_bookmark(
    movie_id: UUID = Path(..., description="Идентификатор фильма", example=uuid.uuid4()),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> None:
    await bookmark_service.add(movie_id)


@router.delete(
    path="/{movie_id}",
    summary="Удаление фильма из закладок",
    status_code=HTTPStatus.OK,
    dependencies=[Depends(HTTPBearer())],
)
async def remove_bookmark(
    movie_id: UUID = Path(..., description="Идентификатор фильма", example=uuid.uuid4()),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> None:
    await bookmark_service.remove(movie_id)


@router.get(
    path="/",
    summary="Получение списока закладок",
    status_code=HTTPStatus.OK,
    dependencies=[Depends(HTTPBearer())],
)
async def get_bookmarks_list(
    page: int = Query(default=1, description="Pagination page number", ge=1),
    page_size: int = Query(
        default=settings.page_size, description="Pagination page size", ge=1, le=settings.page_size_max
    ),
    bookmark_service: BookmarksService = Depends(get_bookmark_service),
) -> BookmarksListResponse:
    return await bookmark_service.list(page, page_size)
