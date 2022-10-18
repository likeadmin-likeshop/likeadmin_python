from fastapi import FastAPI


def configure_event(app: FastAPI):
    from redis import asyncio as aioredis
    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.redis import RedisBackend
    from .config import get_settings
    from .dependencies.database import db

    settings = get_settings()

    @app.on_event('startup')
    async def startup():
        await db.connect()
        redis = aioredis.from_url(settings.redis_url, encoding='utf8', decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix='like')

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()


def configure_router(app: FastAPI, prefix='/api'):
    from .front.routers import index
    from .front.routers import upload
    from .admin.routers import user

    app.include_router(index.router, prefix=prefix)
    app.include_router(upload.router, prefix=prefix)
    app.include_router(user.router, prefix=prefix)


def create_app() -> FastAPI:
    from .exceptions.global_exc import configure_exception

    app = FastAPI()

    configure_exception(app)
    configure_event(app)
    configure_router(app)
    return app
