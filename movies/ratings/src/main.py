from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from http import HTTPStatus

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import ORJSONResponse
# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from api.routers import all_v1_routers
from core.config import settings
# from core.tracer import configure_tracer
# from db import elastic, redis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    #     redis.redis = Redis(host=settings.redis_host, port=settings.redis_port)
    #     elastic.es = AsyncElasticsearch(
    #         hosts=[{"host": settings.elastic_host, "port": settings.elastic_port, "scheme": "http"}],
    #     )
    yield
    #     await redis.redis.close()
    #     await elastic.es.close()
    pass


app = FastAPI(
    title="API для онлайн-кинотеатра для оценок пользователей",
    version="1.0.0",
    docs_url=settings.url_prefix + "/api/openapi",
    redoc_url=settings.url_prefix + "/api/redoc",
    openapi_url=settings.url_prefix + "/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.include_router(all_v1_routers)


# configure_tracer()
# FastAPIInstrumentor.instrument_app(app)
#

@app.middleware("http")
async def before_request(request: Request, call_next: Callable) -> Response:
    if not settings.debug and not request.headers.get("X-Request-Id"):
        return ORJSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={"detail": "X-Request-Id header is required"})
    return await call_next(request)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5000,
    )
