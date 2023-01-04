from wechatpy import WeChatClient

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
