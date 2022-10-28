import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .base import AppException
from ..http_base import HttpResp

logger = logging.getLogger(__name__)


def configure_exception(app: FastAPI):
    """配置全局异常处理
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """处理请求参数验证的异常
            code: 310 311
        """
        resp = HttpResp.PARAMS_VALID_ERROR
        errs = exc.errors()
        if errs and errs[0].get('type', '').startswith('type_error.'):
            resp = HttpResp.PARAMS_TYPE_ERROR
        logger.warning('validation_exception_handler: url=[%s], errs=[%s]', request.url.path, errs)
        return JSONResponse(
            status_code=200,
            content={'code': resp.code, 'msg': resp.msg, 'data': errs})

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """处理客户端请求异常
            code: 312 404
        """
        logger.warning('http_exception_handler: url=[%s], status_code=[%s]', request.url.path, exc.status_code)
        resp = HttpResp.SYSTEM_ERROR
        if exc.status_code == 404:
            resp = HttpResp.REQUEST_404_ERROR
        elif exc.status_code == 405:
            resp = HttpResp.REQUEST_METHOD_ERROR
        return JSONResponse(
            status_code=200,
            content={'code': resp.code, 'msg': resp.msg, 'data': []})

    @app.exception_handler(AssertionError)
    async def assert_exception_handler(request: Request, exc: AssertionError):
        """处理断言异常
            code: 313
        """
        errs = ','.join(exc.args) if exc.args else HttpResp.ASSERT_ARGUMENT_ERROR.msg
        logger.warning('app_exception_handler: url=[%s], errs=[%s]', request.url.path, errs)
        return JSONResponse(
            status_code=200,
            content={'code': HttpResp.ASSERT_ARGUMENT_ERROR.code, 'msg': errs,
                     'data': []})

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """处理自定义异常
            code: .
        """
        if exc.echo_exc:
            logger.error('app_exception_handler: url=[%s]', request.url.path)
            logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=200,
            content={'code': exc.code, 'msg': exc.msg, 'data': []})

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        """处理参数验证的异常 (除请求参数验证之外的)
            code: 500
        """
        logger.error('validation_exception_handler: url=[%s]', request.url.path)
        logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=200,
            content={'code': HttpResp.SYSTEM_ERROR.code, 'msg': HttpResp.SYSTEM_ERROR.code, 'data': []})

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """处理服务端异常, 全局异常处理
            code: 500
        """
        logger.error('global_exception_handler: url=[%s]', request.url.path)
        logger.error(exc, exc_info=True)
        return JSONResponse(
            status_code=200,
            content={'code': HttpResp.SYSTEM_ERROR.code, 'msg': HttpResp.SYSTEM_ERROR.msg, 'data': []})
