from functools import lru_cache
from uuid import UUID

import bson
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends

from pymongo import MongoClient
from db.mongo import get_mongo

from schemas.ratings import RatingsResponse


# # from models.message import Message
# # from schemas.event import CreateEventResponse, UserEvent
from core.config import settings


class RatingService:
    """
    Класс для реализации логики работы с оценками фильмов.
    """

    def __init__(self, jwt: AuthJWT, mongo: MongoClient) -> None:
        self.jwt = jwt
        self.mongo = mongo

    async def like(self, movie_id: UUID) -> None:
        return await self.set_rating(movie_id, 10)

    async def dislike(self, movie_id: UUID) -> None:
        return await self.set_rating(movie_id, 1)

    async def set_rating(self, movie_id: UUID, rating: int) -> None:
        db = self.mongo[settings.mongo_db][settings.mongo_rating_collection]
        db.update_one({
            'movie_id': bson.Binary.from_uuid(movie_id),
            'user_id': (await self.jwt.get_raw_jwt())['sub']
        }, {'$set': {'rating': rating}}, upsert=True)

    async def remove_rating(self, movie_id: UUID) -> None:
        db = self.mongo[settings.mongo_db][settings.mongo_rating_collection]
        db.delete_one({
            'movie_id': bson.Binary.from_uuid(movie_id),
            'user_id': (await self.jwt.get_raw_jwt())['sub']
        })

    async def get_rating(self, movie_id: UUID) -> RatingsResponse:
        # Проверить наличие фильма в базе.
        db = self.mongo[settings.mongo_db][settings.mongo_rating_collection]
        response = RatingsResponse(average=0)
        for rating in db.aggregate([
            {"$match": {"movie_id": bson.Binary.from_uuid(movie_id)}},
            {"$group": {"_id": "$rating", "count": {"$count": {}}}}
        ]):
            if rating['_id'] == 0:
                response.dislikes = rating['count']
            elif rating['_id'] == 10:
                response.likes = rating['count']

            response.average += rating['_id']*rating['count']
            response.count += rating['count']
        if response.count != 0:
            response.average /= response.count

        cursor = db.find_one({
            "movie_id": bson.Binary.from_uuid(movie_id),
            "user_id": (await self.jwt.get_raw_jwt())['sub']
        })
        if cursor:
            response.rating = cursor['rating']
        return response


@lru_cache
def get_rating_service(
    jwt: AuthJWT = Depends(),
    mongo: MongoClient = Depends(get_mongo),
) -> RatingService:
    return RatingService(jwt, mongo)
