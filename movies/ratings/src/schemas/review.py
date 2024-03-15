from pydantic import Field, BaseModel, ConfigDict

class ReviewData(BaseModel):
    review: str = Field(
        description="Текст рецензии на фильм",
        examples=["Этот фильм просто отвратительный!"]
    )


class ReviewRequest(ReviewData):
    rating: int | None = Field(
        default=None,
        description="Оценка фильма",
        examples=[7]
    )


class ReviewCreatedResponse(BaseModel):
    """Количества лайков у фильма"""
    review_id: str = Field(
        description="Идентификатор рецензии",
        examples=["65f3964582f344ecf4de0c5c"]
    )
