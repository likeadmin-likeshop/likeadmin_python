from abc import ABC, abstractmethod

from like.admin.schemas.channel import ChannelMpIn
from like.config import get_settings
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IChannelMpService(ABC):
    """微信小程序渠道服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, mp_in: ChannelMpIn):
        pass


class ChannelMpService(IChannelMpService):
    """微信小程序渠道服务实现类"""

    async def detail(self) -> dict:
        """微信小程序渠道详情"""
        is_prod = get_settings().mode == 'prod'

        config = await ConfigUtil.get('mp_channel')
        config['name'] = config.get('name', '')
        config['primaryId'] = config.get('primaryId', '')
        config['appId'] = '******' if is_prod else config.get('appId', '')
        config['appSecret'] = '******' if is_prod else config.get('appSecret', '')
        config['qrCode'] = await UrlUtil.to_absolute_url(config.get('qrCode', ''))

        domain = get_settings().domain
        config['requestDomain'] = domain
        config['socketDomain'] = domain
        config['uploadFileDomain'] = domain
        config['downloadFileDomain'] = domain
        config['udpDomain'] = domain
        config['tcpDomain'] = domain
        config['businessDomain'] = domain
        return config

    async def save(self, mp_in: ChannelMpIn):
        """微信小程序渠道保存"""
        await ConfigUtil.set('mp_channel', 'name', str(mp_in.name))
        await ConfigUtil.set('mp_channel', 'primaryId', str(mp_in.primary_id))
        await ConfigUtil.set('mp_channel', 'appId', mp_in.app_id)
        await ConfigUtil.set('mp_channel', 'appSecret', mp_in.app_secret)
        await ConfigUtil.set('mp_channel', 'qrCode', await UrlUtil.to_relative_url(mp_in.qr_code))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
