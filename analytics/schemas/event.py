import time as tm

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import Dict


def get_now_in_ms() -> int:
    return round(tm.time() * 1000)


class UserEvent(BaseModel):
    """Пользовательское событие"""

    """Время пользовательского события"""
    timestamp: int | None = Field(
        ...,
        default_factory=get_now_in_ms,
        description="Метка времени события в ms",
        example=1708767326343,
    )
    """UUID фильма в формате str"""
    film_id: str | None = Field(
        None,
        description="Идентификатор фильма",
        example="3d825f60-9fff-4dfe-b294-1a45fa1e115d",
    )
    """Значение пользовательского события"""
    value: Dict[str, str] | None = Field(
        None,
        description="Метаданные пользовательского события в формате Dict[str, str]",
        example={"view_uri": "/films/favourites", "view_duration": "4561"},
    )

    model_config = ConfigDict(from_attributes=True)


class CreateEventResponse(BaseModel):
    """Ответ на создание события"""

    event_sent: bool = Field(
        ...,
        description="Сообщение отправлено в кластер Kafka",
        example=True,
    )

    model_config = ConfigDict(from_attributes=True)


class HealthCheckResponse(BaseModel):
    """Статус работы"""
    status: str
