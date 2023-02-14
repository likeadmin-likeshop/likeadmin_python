from abc import ABC, abstractmethod

from like.admin.schemas.channel import ChannelOaIn
from like.config import get_settings
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IChannelOaService(ABC):
    """公众号渠道设置服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, oa_in: ChannelOaIn):
        pass


class ChannelOaService(IChannelOaService):
    """公众号渠道设置服务实现类"""

    async def detail(self) -> dict:
        """公众号渠道设置详情"""
        config = await ConfigUtil.get('oa_channel')
        config.pop('menus')
        config['qrCode'] = await UrlUtil.to_absolute_url(config.get('qrCode', ''))
        config['name'] = config.get('name', '')
        config['primaryId'] = config.get('primaryId', '')
        config['appId'] = config.get('appId', '')
        config['appSecret'] = config.get('appSecret', '')
        config['url'] = config.get('url', '')
        config['token'] = config.get('token', '')
        config['encodingAesKey'] = config.get('encodingAesKey', '')
        config['encryptionType'] = int(config.get('encryptionType', '1'))
        config['businessDomain'] = get_settings().domain
        config['jsDomain'] = get_settings().domain
        config['webDomain'] = get_settings().domain
        return config

    async def save(self, oa_in: ChannelOaIn):
        """公众号渠道设置保存"""
        await ConfigUtil.set('oa_channel', 'name', oa_in.name)
        await ConfigUtil.set('oa_channel', 'primaryId', oa_in.primary_id)
        await ConfigUtil.set('oa_channel', 'qrCode', oa_in.qr_code)
        await ConfigUtil.set('oa_channel', 'appId', oa_in.app_id)
        await ConfigUtil.set('oa_channel', 'appSecret', oa_in.app_secret)
        await ConfigUtil.set('oa_channel', 'url', oa_in.url)
        await ConfigUtil.set('oa_channel', 'token', oa_in.token)
        await ConfigUtil.set('oa_channel', 'encodingAesKey', oa_in.encoding_aes_key)
        await ConfigUtil.set('oa_channel', 'encryptionType', str(oa_in.encryption_type))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
