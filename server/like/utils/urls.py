from like.config import get_settings


class UrlUtil:
    engine = 'local'
    domain: str = get_settings().domain
    upload_prefix: str = get_settings().upload_prefix

    @classmethod
    def to_absolute_url(cls, url: str) -> str:
        """
        转绝对路径
        转前: /uploads/11.png
        转后: https://127.0.0.1/uploads/11.png
        TODO: 目前仅考虑engine=local情况
        :param url: 相对路径
        :return:
        """
        if not url:
            return ''
        if url.find('/') != 0:
            url = '/' + url
        if url.startswith('/api/static/'):
            return cls.domain + url
        return cls.domain + cls.upload_prefix + url

    @classmethod
    def to_relative_url(cls, url: str) -> str:
        """
        转相对路径
        转前: https://127.0.0.1/uploads/11.png
        转后: /uploads/11.png
        TODO: 目前仅考虑engine=local情况
        :param url:
        :return:
        """
        if not url or not url.startswith('http'):
            return url
        if cls.engine == 'local':
            return url.replace(cls.domain, '').replace('/' + cls.upload_prefix + '/', '/')
        return url
