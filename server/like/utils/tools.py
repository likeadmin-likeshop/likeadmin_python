from typing import Final
import string
import hashlib
import random
import time
import uuid

from like.config import get_settings


ALL_RANDOM_STR: Final[str] = string.ascii_letters + string.digits


class ToolsUtil:
    secret: Final[str] = get_settings().secret

    @staticmethod
    def random_string(length: int) -> str:
        return ''.join(random.choices(ALL_RANDOM_STR, k=length))

    @staticmethod
    def make_uuid() -> str:
        return uuid.uuid4().hex

    @staticmethod
    def make_md5(data: str) -> str:
        hl_md5 = hashlib.md5()
        hl_md5.update(data.encode('utf-8'))
        return hl_md5.hexdigest()

    @staticmethod
    def make_token() -> str:
        ms = int(time.time() * 1000)
        token = ToolsUtil.make_md5(f'{ToolsUtil.make_uuid()}{ms}{ToolsUtil.random_string(8)}')
        token_secret = f'{token}{ToolsUtil.secret}'
        return f'{ToolsUtil.make_md5(token_secret)}{ToolsUtil.random_string(6)}'
