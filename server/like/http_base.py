from collections import namedtuple
from functools import wraps

__all__ = ['HttpCode', 'HttpResp', 'unified_resp']

HttpCode = namedtuple('HttpResp', ['code', 'msg'])


class HttpResp:
    """HTTP响应结果
    """
    SUCCESS = HttpCode(200, '成功')
    FAILED = HttpCode(300, '失败')
    PARAMS_VALID_ERROR = HttpCode(310, '参数校验错误')
    PARAMS_TYPE_ERROR = HttpCode(311, '参数类型错误')
    REQUEST_METHOD_ERROR = HttpCode(312, '请求方法错误')
    # ASSERT_ARGUMENT_ERROR = HttpResp(313, '断言参数错误')

    LOGIN_ACCOUNT_ERROR = HttpCode(330, '登录账号或密码错误')
    LOGIN_DISABLE_ERROR = HttpCode(331, '登录账号已被禁用了')
    TOKEN_EMPTY = HttpCode(332, 'token参数为空')
    TOKEN_INVALID = HttpCode(333, 'token参数无效')

    NO_PERMISSION = HttpCode(403, '无相关权限')
    REQUEST_404_ERROR = HttpCode(404, '请求接口不存在')

    SYSTEM_ERROR = HttpCode(500, '系统错误')


def unified_resp(func):
    """统一响应格式
        接口正常返回时,统一响应结果格式
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        resp = await func(*args, **kwargs) or []
        return {'code': HttpResp.SUCCESS.code, 'msg': HttpResp.SUCCESS.msg, 'data': resp}

    return wrapper
