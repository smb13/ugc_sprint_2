from enum import Enum

from pydantic import Field, BaseModel, ConfigDict


class ReviewRequest(BaseModel):
    review: str = Field(
        description="Текст рецензии на фильм",
        examples=["Этот фильм просто отвратительный!"]
    )


class ReviewSortKeys(str, Enum):
    average_asc = "rating"
    avergae_desc = "-rating"
    likes_asc = "likes"
    likes_desc = "-likes"
    dislikes_asc = "dislikes"
    dislikes_desc = "-dislikes"


class ReviewResponse(ReviewRequest):
    """
        Результат запроса рецензии.
    """

    """Количество лайков у рецензии"""
    likes: int | None = Field(
        0,
        description="Количества лайков у фильма",
        example=1,
    )
    """Количество дизлайков у рецензии"""
    dislikes: int | None = Field(
        0,
        description="Количества дизлайков у фильма",
        example=123,
    )
    """Средняя пользовательская оценка фильма"""
    average: float | None = Field(
        0,
        description="Средняя пользовательская оценка фильма",
        example=2.3,
    )


class ReviewList(BaseModel):
    """
        Список отзывов
    """

    total: int = Field(
        default=0,
        description="Общее число найденных отзывов",
        example=17
    )

    reviews: list[ReviewResponse] = Field(
        description="Список отзывов"
    )