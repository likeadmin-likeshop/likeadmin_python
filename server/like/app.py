import os

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
    from .middlewares import init_cors_middleware, init_timeout_middleware

    app.add_middleware(ProxyHeadersMiddleware)
    init_cors_middleware(app)
    init_timeout_middleware(app)


def configure_static(app: FastAPI):
    """配置静态资源"""
    from .config import get_settings
    settings = get_settings()
    # 上传路径创建
    if not os.path.exists(settings.upload_directory):
        os.makedirs(settings.upload_directory)
    # 上传路径配置
    app.mount(settings.upload_prefix, StaticFiles(directory=settings.upload_directory), name='upload')
    # 静态资源路径配置
    if settings.enabled_static:
        app.mount(settings.static_path, StaticFiles(directory=settings.static_directory), name='static')


def configure_admin_router(app: FastAPI, prefix='/api'):
    """配置后台路由"""
    from .dependencies.verify import verify_token, verify_show_mode
    from .config import get_settings
    from .admin.routers import user, common, system, monitor, setting, article as admin_article
    from .generator.routers import gen

    settings = get_settings()
    # 后台依赖
    admin_deps = [Depends(verify_token)]
    if settings.disallow_modify:
        admin_deps.append(Depends(verify_show_mode))
    # admin
    app.include_router(user.router, prefix=prefix, dependencies=admin_deps)
    app.include_router(common.router, prefix=prefix, dependencies=admin_deps)
    app.include_router(system.router, prefix=prefix, dependencies=admin_deps)
    app.include_router(monitor.router, prefix=prefix, dependencies=admin_deps)
    app.include_router(setting.router, prefix=prefix, dependencies=admin_deps)
    app.include_router(admin_article.router, prefix=prefix, dependencies=admin_deps)
    # gen
    app.include_router(gen.router, prefix=prefix, dependencies=admin_deps)


def configure_front_router(app: FastAPI, prefix='/api'):
    """配置前台路由"""
    from .dependencies.verify import front_login_verify
    from .front.routers import index, upload, article as front_article, login

    # front 依赖
    front_deps = [Depends(front_login_verify)]
    # front
    app.include_router(index.router, prefix=prefix, dependencies=front_deps)
    app.include_router(upload.router, prefix=prefix, dependencies=front_deps)
    app.include_router(front_article.router, prefix=prefix, dependencies=front_deps)
    app.include_router(login.router, prefix=prefix, dependencies=front_deps)


def create_app() -> FastAPI:
    """创建FastAPI后台应用,并初始化"""
    from .exceptions.global_exc import configure_exception

    app = FastAPI()
    configure_static(app)
    configure_exception(app)
    configure_event(app)
    configure_middleware(app)
    configure_admin_router(app)
    add_pagination(app)
    return app


def create_front() -> FastAPI:
    """创建FastAPI前台应用,并初始化"""
    from .exceptions.global_exc import configure_exception

    app = FastAPI()
    configure_static(app)
    configure_exception(app)
    configure_event(app)
    configure_middleware(app)
    configure_front_router(app)
    add_pagination(app)
    return app
