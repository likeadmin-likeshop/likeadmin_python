import hashlib
import json
import random
import string
import time
import uuid
from typing import Union

from like.config import get_settings

ALL_RANDOM_STR: str = string.ascii_letters + string.digits


class ToolsUtil:
    """常用工具集合类"""
    secret: str = get_settings().secret

    @staticmethod
    def random_string(length: int) -> str:
        """返回随机字符串"""
        return ''.join(random.choices(ALL_RANDOM_STR, k=length))

    @staticmethod
    def random_int(length: int) -> int:
        """
        返回指定长度的随机整数
        :param length:
        :return:
        """
        return random.randint(0, 10 ** length)

    @staticmethod
    def make_uuid() -> str:
        """制作UUID"""
        return uuid.uuid4().hex

    @staticmethod
    def make_md5(data: str) -> str:
        """制作MD5"""
        hl_md5 = hashlib.md5()
        hl_md5.update(data.encode('utf-8'))
        return hl_md5.hexdigest()

    @staticmethod
    def make_token() -> str:
        """生成唯一Token"""
        ms = int(time.time() * 1000)
        token = ToolsUtil.make_md5(f'{ToolsUtil.make_uuid()}{ms}{ToolsUtil.random_string(8)}')
        token_secret = f'{token}{ToolsUtil.secret}'
        return f'{ToolsUtil.make_md5(token_secret)}{ToolsUtil.random_string(6)}'

    @staticmethod
    def json_to_map(json_str: str) -> Union[dict, list]:
        """JSON转dict"""
        return json.loads(json_str)
