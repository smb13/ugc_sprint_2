# from functools import lru_cache
# from uuid import UUID
#
# import bson
# from async_fastapi_jwt_auth import AuthJWT
# from fastapi import Depends
#
# from pymongo import MongoClient
# from db.mongo import get_mongo
#
# from schemas.ratings import RatingsResponse
#
# from core.config import settings
#
#
# class RatingService:
#     """
#     Класс для реализации логики работы с оценками фильмов.
#     """
#
#     def __init__(self, jwt: AuthJWT, mongo: MongoClient) -> None:
#         self.jwt = jwt
#         self.mongo = mongo
#
#     async def like(self, movie_id: UUID) -> None:
#         return await self.set_rating(movie_id, 10)
#
#     async def dislike(self, movie_id: UUID) -> None:
#         return await self.set_rating(movie_id, 1)
#
#     async def set_rating(self, movie_id: UUID, rating: int) -> None:
#         db = self.mongo[settings.mongo_db][settings.mongo_rating_collection]
#         db.update_one({
#             'movie_id': bson.Binary.from_uuid(movie_id),
#             'user_id': (await self.jwt.get_raw_jwt())['sub']
#         }, {'$set': {'rating': rating}}, upsert=True)
#
#     async def remove_rating(self, movie_id: UUID) -> None:
#         db = self.mongo[settings.mongo_db][settings.mongo_rating_collection]
#         db.delete_one({
#             'movie_id': bson.Binary.from_uuid(movie_id),
#             'user_id': (await self.jwt.get_raw_jwt())['sub']
#         })
#
#     async def get_rating(self, movie_id: UUID) -> RatingsResponse:
#         db = self.mongo[settings.mongo_db][settings.mongo_rating_collection]
#         for rating in db.aggregate([
#             {"$match": {"movie_id": bson.Binary.from_uuid(movie_id)}},
#             {"$group": {
#                 "_id": "$movie_id",
#                 "total": {"$sum": 1},
#                 "likes": {"$sum": {"$cond": [{"$eq": ["$rating", 10]}, 1, 0]}},
#                 "dislikes": {"$sum": {"$cond": [{"$eq": ["$rating", 1]}, 1, 0]}},
#                 "average": {"$avg": "$rating"},
#                 "rating": {
#                     "$sum": {"$cond": [{"$eq": ["$user_id", (await self.jwt.get_raw_jwt())['sub']]}, "$rating", 0]}}}}
#         ]):
#             return RatingsResponse(**rating)
#         return RatingsResponse()
#
#
# @lru_cache
# def get_rating_service(
#     jwt: AuthJWT = Depends(),
#     mongo: MongoClient = Depends(get_mongo),
# ) -> RatingService:
#     return RatingService(jwt, mongo)
