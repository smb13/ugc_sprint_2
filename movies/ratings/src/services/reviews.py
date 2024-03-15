from functools import lru_cache
from uuid import UUID

# import bson
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends

from pymongo import MongoClient
from db.mongo import get_mongo
from schemas.review import ReviewCreatedResponse, ReviewData
from services.base import BaseService


class ReviewService(BaseService):
    """
    Класс для реализации логики работы с рецензиями на фильмы.
    """

    async def add_review(self, movie_id: UUID, review: str, rating: int) -> ReviewCreatedResponse:
        return ReviewCreatedResponse(review_id="111")

    async def remove_review(self, movie_id: UUID) -> None:
        pass

    async def like(self, movie_id: UUID, review_id: str) -> None:
        pass

    async def dislike(self, movie_id: UUID, review_id: str) -> None:
        pass

    async def get_review(self, movie_id: UUID) -> ReviewData:
        return ReviewData()

    async def get_review_list(self, movie_id: UUID) -> list[ReviewData]:
        return []


@lru_cache
def get_review_service(
    jwt: AuthJWT = Depends(),
    mongo: MongoClient = Depends(get_mongo),
) -> ReviewService:
    return ReviewService(jwt, mongo)
