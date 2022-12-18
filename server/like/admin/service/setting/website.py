from abc import ABC, abstractmethod

from like.admin.schemas.setting import SettingWebsiteIn
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class ISettingWebsiteService(ABC):
    """网站信息配置服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, website_in: SettingWebsiteIn):
        pass


class SettingWebsiteService(ISettingWebsiteService):
    """网站信息配置服务实现类"""

    async def detail(self) -> dict:
        """获取网站信息"""
        config = await ConfigUtil.get('website')
        return {
            'name': config.get('name', ''),
            'logo': await UrlUtil.to_absolute_url(config.get('logo', '')),
            'favicon': await UrlUtil.to_absolute_url(config.get('favicon', '')),
            'backdrop': await UrlUtil.to_absolute_url(config.get('backdrop', '')),
            'shopName': config.get('shopName', ''),
            'shopLogo': await UrlUtil.to_absolute_url(config.get('shopLogo', '')),
        }

    async def save(self, website_in: SettingWebsiteIn):
        """保存网站信息"""
        await ConfigUtil.set('website', 'name', website_in.name)
        await ConfigUtil.set('website', 'logo', await UrlUtil.to_relative_url(website_in.logo))
        await ConfigUtil.set('website', 'favicon', await UrlUtil.to_relative_url(website_in.favicon))
        await ConfigUtil.set('website', 'backdrop', await UrlUtil.to_relative_url(website_in.backdrop))
        await ConfigUtil.set('website', 'shopName', website_in.shop_name)
        await ConfigUtil.set('website', 'shopLogo', await UrlUtil.to_relative_url(website_in.shop_logo))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
