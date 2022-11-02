from typing import Final

from like.config import get_settings


class UrlUtil():
    engine = 'local'
    domain: Final[str] = get_settings().domain
    upload_prefix: Final[str] = get_settings().upload_prefix

    def to_absolute_url(self, url: str) -> str:
        """
        转绝对路径
        转前: uploads/11.png
        转后: https://127.0.0.1/uploads/11.png
        TODO: 目前仅考虑engine=local情况
        :param url: 相对路径
        :return:
        """
        if not url:
            return ""
        if url.index("/") != 0:
            url = "/" + url
        if url.startswith("/api/static/"):
            return self.domain + '/' + self.upload_prefix
        return self.domain + '/' + self.upload_prefix + url

    def to_relative_url(self, url: str) -> str:
        """
        转相对路径
        转前: https://127.0.0.1/uploads/11.png
        转后: uploads/11.png
        TODO: 目前仅考虑engine=local情况
        :param url:
        :return:
        """
        if not url or url.startswith('http'):
            return url
        if self.engine == 'local':
            return url.replace(self.domain, "").replace("/" + self.upload_prefix + "/", "/")
        return url
