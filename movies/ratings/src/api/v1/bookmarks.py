from http import HTTPStatus
# from typing import Annotated
from uuid import UUID
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Path
#
# from api.v1.fields import PageNumberQueryType, PageSizeQueryType
# from api.v1.models import FilmDetailExternal, FilmPersonExternal, FilmShortExternal, FilmsSortKeys, GenreExternal
# from core.auth import JWTTokenPayload, SystemRolesEnum, check_permissions
# from core.config import settings
# from core.types import NestedQuery, RequestData
# from models.film import Film as FilmInternal
# from services.base import BaseService
# from services.films import get_films_service

# from uuid import UUID

from fastapi.security import HTTPBearer

# from schemas.ratings import RatingsResponse
# from services.ratings import RatingService, get_rating_service

router = APIRouter(redirect_slashes=False)


@router.post(
    path="/{movie_id}",
    summary="Добавление фильма в закладки",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(HTTPBearer())],
)
async def add_bookmark(
    movie_id: UUID = Path(..., description="Идентификатор фильма", example=uuid.uuid4()),
    # rating_service: RatingService = Depends(get_rating_service),
) -> None:
    # await rating_service.set_like(movie_id)
    pass


@router.delete(
    path="/{movie_id}",
    summary="Удаление фильма из закладок",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(HTTPBearer())],
)
async def like_movie(
    movie_id: UUID = Path(..., description="Идентификатор фильма", example=uuid.uuid4()),
    # rating_service: RatingService = Depends(get_rating_service),
) -> None:
    # await rating_service.set_dislike(movie_id)
    pass


@router.get(
    path="/",
    summary="Получение списка закладок",
    status_code=HTTPStatus.CREATED,
    dependencies=[Depends(HTTPBearer())],
)
async def like_movie(
    # rating_service: RatingService = Depends(get_rating_service),
) -> None:
    # await rating_service.set_rating(movie_id, rating)
    pass


# @router.get(
#     path="/{movie_id}",
#     summary="Получение рейтинга фильма",
#     status_code=HTTPStatus.OK,
#     dependencies=[Depends(HTTPBearer())],
# )
# async def get_ratings(
#     movie_id: UUID = Path(..., description="Идентификатор фильма", example=uuid.uuid4()),
#     rating_service: RatingService = Depends(get_rating_service),
# ) -> RatingsResponse:
#     return await rating_service.get_rating(movie_id)