from typing_extensions import Final

from like.config import get_settings
from like.utils.config import ConfigUtil


class UrlUtil:
    domain: Final[str] = get_settings().domain
    upload_prefix: Final[str] = get_settings().upload_prefix
    engine = 'local'

    @classmethod
    async def to_absolute_url(cls, url: str, engine='local') -> str:
        """
        转绝对路径
        转前: /uploads/11.png
        转后: https://127.0.0.1/uploads/11.png
        :param url: 相对路径
        :return:
        """
        if not url:
            return ''
        if url.find('/') != 0:
            url = '/' + url
        if url.startswith('/api/static/'):
            return cls.domain + url
        if not engine:
            engine = await ConfigUtil.get_val("storage", "default", "local")
        if engine == 'local':
            return cls.domain + cls.upload_prefix + url
        config = await ConfigUtil.get_map("storage", engine)
        return config.get('domain') + url

    @classmethod
    async def to_relative_url(cls, url: str, engine=None) -> str:
        """
        转相对路径
        转前: https://127.0.0.1/uploads/11.png
        转后: /uploads/11.png
        :param url:
        :return:
        """
        if not url or not url.startswith('http'):
            return url
        if not engine:
            engine = await ConfigUtil.get_val("storage", "default", "local")
        if engine == 'local':
            return url.replace(get_settings().domain, '').replace('/' + cls.upload_prefix + '/', '/')
        config = await ConfigUtil.get_map("storage", engine)
        if config:
            return url.replace(config.get("domain", ""), "").replace("/" + cls.upload_prefix + "/", "")
        return url
