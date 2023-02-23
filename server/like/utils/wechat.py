from wechatpy import WeChatClient
from wechatpy.client.api import WeChatWxa

from like.utils.config import ConfigUtil

__all__ = ['WeChatUtil']


class WeChatUtil:
    """微信工具"""

    @staticmethod
    async def official() -> WeChatClient:
        """微信公众号"""
        config = await ConfigUtil.get('oa_channel')
        return WeChatClient(
            config.get('appId', ''),
            config.get('appSecret', ''))

    @staticmethod
    async def mnp() -> WeChatWxa:
        """微信小程序"""
        config = await ConfigUtil.get("mp_channel")
        client = WeChatClient(
            config.get('appId', ''),
            config.get('appSecret', ''))
        return client.wxa
