"""全局异常处理
"""
import logging

from ..http_base import HttpCode, HttpResp


__all__ = ['AppException']


logger = logging.getLogger(__name__)


class AppException(Exception):
    """The App Exception
    """

    def __init__(self, exc: HttpCode, *args, **kwargs):
        super().__init__()
        self._code = exc.code or HttpResp.FAILED.code
        self._message = exc.msg or HttpResp.FAILED.msg
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
