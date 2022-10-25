"""全局异常处理
"""
import logging

from ..http_base import HttpCode, HttpResp

__all__ = ['AppException']

logger = logging.getLogger(__name__)


class AppException(Exception):
    """应用异常基类
    """

    def __init__(self, exc: HttpCode, *args, code: int = None, msg: str = None, echo_exc: bool = False, **kwargs):
        super().__init__()
        _code = code if code is not None else exc.code
        _message = msg if msg is not None else exc.msg
        self._code = _code or HttpResp.FAILED.code
        self._message = _message or HttpResp.FAILED.msg
        self.echo_exc = echo_exc
        self.args = args or []
        self.kwargs = kwargs or {}

    @property
    def code(self) -> int:
        return self._code

    @property
    def msg(self) -> str:
        return self._message

    def __str__(self):
        return '{}: {}'.format(self.code, self.msg)
