import datetime as dt
import json
import uuid
from typing import Any

from pydantic import BaseModel, field_serializer


class Event(BaseModel):
    user_id: str | None
    timestamp: dt.datetime
    value: dict[str, Any] | None

    @field_serializer("value")
    def serialize_value(self, value: dict[str, Any]) -> str:
        return json.dumps(value)

    @field_serializer("timestamp")
    def serialize_timestamp(self, timestamp: dt.datetime) -> int:
        return int(timestamp.timestamp())


class User(Event):
    pass


class Film(Event):
    film_id: uuid.UUID

    @field_serializer("film_id")
    def serialize_film_id(self, film_id: uuid.UUID) -> str:
        return str(film_id)
