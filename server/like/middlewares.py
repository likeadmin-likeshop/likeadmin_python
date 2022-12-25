import asyncio
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from .http_base import HttpResp


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


class TimeoutMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, timeout: int = 15):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request, call_next):
        try:
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return JSONResponse(
                {'code': HttpResp.SYSTEM_TIMEOUT_ERROR.code, 'msg': HttpResp.SYSTEM_TIMEOUT_ERROR.msg, 'data': []})


def init_timeout_middleware(app: FastAPI):
    """初始化 超时处理 中间件"""
    from .config import get_settings
    app.add_middleware(
        TimeoutMiddleware,
        timeout=get_settings().request_timeout)
