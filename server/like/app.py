from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination


def configure_event(app: FastAPI):
    """配置事件处理, 并初始化三方库"""
    from fastapi_cache import FastAPICache
    from .config import get_settings
    from .dependencies.database import db
    from .dependencies.cache import redis_be, custom_key_builder

    settings = get_settings()

    @app.on_event('startup')
    async def startup():
        await db.connect()
        FastAPICache.init(redis_be, prefix=settings.redis_prefix, key_builder=custom_key_builder)

    @app.on_event('shutdown')
    async def shutdown():
        await db.disconnect()


def configure_middleware(app: FastAPI):
    """配置中间件"""
    from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

    app.add_middleware(ProxyHeadersMiddleware)


def configure_router(app: FastAPI, prefix='/api'):
    """配置路由"""
    from .front.routers import index
    from .front.routers import upload
    from .admin.routers import user, common, system

    app.include_router(index.router, prefix=prefix)
    app.include_router(upload.router, prefix=prefix)
    app.include_router(user.router, prefix=prefix)
    app.include_router(common.router, prefix=prefix)
    app.include_router(system.router, prefix=prefix)


def create_app() -> FastAPI:
    """创建FastAPI应用,并初始化"""
    from .config import get_settings
    from .exceptions.global_exc import configure_exception
    from .dependencies.verify import verify_token

    app = FastAPI(dependencies=[Depends(verify_token)])

    settings = get_settings()
    # 静态资源路径配置
    if settings.enabled_static:
        app.mount(settings.static_path, StaticFiles(directory=settings.static_directory), name='static')

    configure_exception(app)
    configure_event(app)
    configure_middleware(app)
    configure_router(app)
    add_pagination(app)
    return app
