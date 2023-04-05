from abc import ABC, abstractmethod

from like.admin.schemas.channel import ChannelWxIn
from like.config import get_settings
from like.utils.config import ConfigUtil


class IChannelWxService(ABC):
    """微信开放平台设置服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, wx_in: ChannelWxIn):
        pass


class ChannelWxService(IChannelWxService):
    """微信开放平台设置服务实现类"""

    async def detail(self) -> dict:
        """微信开放平台设置详情"""
        is_prod = get_settings().mode == 'prod'

        config = await ConfigUtil.get('wx_channel')
        config['appId'] = '******' if is_prod else config.get('appId', '')
        config['appSecret'] = '******' if is_prod else config.get('appSecret', '')
        return config

    async def save(self, wx_in: ChannelWxIn):
        """微信开放平台设置保存"""
        await ConfigUtil.set('wx_channel', 'appId', str(wx_in.app_id))
        await ConfigUtil.set('wx_channel', 'appSecret', str(wx_in.app_secret))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
