import inspect
from collections import namedtuple
from datetime import datetime
from functools import wraps
from typing import Callable, TypeVar

import pytz
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .config import get_settings

__all__ = ['HttpCode', 'HttpResp', 'unified_resp']

RT = TypeVar('RT')  # 返回类型
HttpCode = namedtuple('HttpResp', ['code', 'msg'])


class HttpResp:
    """HTTP响应结果
    """
    SUCCESS = HttpCode(200, '成功')
    FAILED = HttpCode(300, '失败')
    PARAMS_VALID_ERROR = HttpCode(310, '参数校验错误')
    PARAMS_TYPE_ERROR = HttpCode(311, '参数类型错误')
    REQUEST_METHOD_ERROR = HttpCode(312, '请求方法错误')
    ASSERT_ARGUMENT_ERROR = HttpCode(313, '断言参数错误')

    LOGIN_ACCOUNT_ERROR = HttpCode(330, '登录账号或密码错误')
    LOGIN_DISABLE_ERROR = HttpCode(331, '登录账号已被禁用了')
    TOKEN_EMPTY = HttpCode(332, 'token参数为空')
    TOKEN_INVALID = HttpCode(333, 'token参数无效')

    NO_PERMISSION = HttpCode(403, '无相关权限')
    REQUEST_404_ERROR = HttpCode(404, '请求接口不存在')

    SYSTEM_ERROR = HttpCode(500, '系统错误')
    SYSTEM_TIMEOUT_ERROR = HttpCode(504, '请求超时')


def unified_resp(func: Callable[..., RT]) -> Callable[..., RT]:
    """统一响应格式
        接口正常返回时,统一响应结果格式
    """

    @wraps(func)
    async def wrapper(*args, **kwargs) -> RT:
        if inspect.iscoroutinefunction(func):
            resp = await func(*args, **kwargs) or []
        else:
            resp = func(*args, **kwargs) or []
        return JSONResponse(
            content=jsonable_encoder(
                # 正常请求响应
                {'code': HttpResp.SUCCESS.code, 'msg': HttpResp.SUCCESS.msg, 'data': resp},
                by_alias=False,
                # 自定义日期时间格式编码器
                custom_encoder={
                    datetime: lambda dt: dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(get_settings().timezone))
                    .strftime(get_settings().datetime_fmt)}),
            media_type='application/json;charset=utf-8'
        )

    return wrapper
