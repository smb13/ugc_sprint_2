from pydantic import Field, BaseModel, ConfigDict


class ReviewRequest(BaseModel):
    review: str = Field(
        description="Текст рецензии на фильм",
        examples=["Этот фильм просто отвратительный!"]
    )

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
