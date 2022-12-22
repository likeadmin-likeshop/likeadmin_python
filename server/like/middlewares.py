import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_cors_middleware(app: FastAPI):
    """初始化 CORS（跨域资源共享）中间件"""
    from .config import get_settings
    app.add_middleware(
        CORSMiddleware,
        allow_origins=json.loads(get_settings().cors_allow_origins),
        allow_headers=['*'],
        allow_methods=['OPTIONS', 'GET', 'POST', 'DELETE', 'PUT'],
        max_age=3600
    )
