from abc import ABC, abstractmethod

from like.admin.schemas.channel import ChannelH5In
from like.utils.config import ConfigUtil


class IChannelH5Service(ABC):
    """H5渠道设置服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, h5_in: ChannelH5In):
        pass


class ChannelH5Service(IChannelH5Service):
    """H5渠道设置服务实现类"""

    async def detail(self) -> dict:
        """公众号渠道设置详情"""
        config = await ConfigUtil.get('h5_channel')
        config['status'] = int(config.get('status')) if config.get('status').isdigit() else 0
        config['close'] = int(config.get('close')) if config.get('close').isdigit() else 0
        config['url'] = config.get('url', '')
        return config

    async def save(self, h5_in: ChannelH5In):
        """公众号渠道设置保存"""
        await ConfigUtil.set('h5_channel', 'status', str(h5_in.status))
        await ConfigUtil.set('h5_channel', 'close', str(h5_in.close))
        await ConfigUtil.set('h5_channel', 'url', h5_in.url)

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
