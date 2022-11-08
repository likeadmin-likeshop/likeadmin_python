import json
import logging
import time
from enum import Enum, unique
from typing import Callable

from fastapi import Request

__all__ = ['RequestType', 'record_log']

logger = logging.getLogger(__name__)

EMPTY_FUNC = lambda: None


@unique
class RequestType(Enum):
    """请求参数类"""
    File = 'file'  # 文件类型
    Default = 'default'  # 默认数据类型


def record_log(title: str = '', req_type: RequestType = RequestType.Default) -> Callable:
    """记录系统日志信息"""
    from like.dependencies.database import db
    from like.models import system_log_operate

    async def dep_func(request: Request):
        # 开始时间
        start_time = time.time()
        # 异常
        err = None
        # 异常信息
        error = ''
        status = 1  # 1=成功, 2=失败
        args = ''
        # 请求方式
        req_method = request.method
        logger.error('record_log before')
        # 获取请求参数
        if req_method == 'POST':
            if req_type == RequestType.File:
                # 文件类型
                forms = await request.form()
                # args = json.dumps({k: v.filename for k, v in forms.items()}, ensure_ascii=False)
                # 获取文件名称作为参数
                args = ','.join([i.filename for i in forms.values()])
            else:
                form_params = await request.json()
                args = json.dumps([form_params], ensure_ascii=False)
        elif req_method == 'GET':
            # args = json.dumps(dict(request.query_params), ensure_ascii=False)
            args = str(request.query_params)
        # 执行方法
        try:
            yield
        except Exception as e:
            err = e
            error = str(e)
            status = 2
        logger.error('record_log after')
        # 结束时间
        end_time = time.time()
        # 执行时间(毫秒)
        task_time = (end_time - start_time) * 1000
        # 获取当前的用户
        admin_id = request.state.admin_id
        url = request.url.path
        ip = request.client.host
        endpoint = request.scope.get('endpoint', EMPTY_FUNC)
        # 执行函数
        method = f'{endpoint.__module__}.{endpoint.__name__}()'
        await db.execute(system_log_operate.insert().values(
            admin_id=admin_id, type=req_method, title=title, ip=ip, url=url, method=method, args=args, error=error,
            status=status, start_time=int(start_time), end_time=int(end_time), task_time=int(task_time),
            create_time=int(time.time())))
        # 执行出现异常则抛出
        if err:
            raise err

    return dep_func
