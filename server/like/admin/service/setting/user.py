from abc import ABC, abstractmethod

from like.admin.schemas.setting import SettingUserIn
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class ISettingUserService(ABC):
    """用户设置服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, user_in: SettingUserIn):
        pass


class SettingUserService(ISettingUserService):
    """用户设置服务实现类"""

    async def detail(self) -> dict:
        """用户设置详情"""
        return {
            'defaultAvatar': await UrlUtil.to_absolute_url(await ConfigUtil.get_val('user', 'defaultAvatar', '')),
        }

    async def save(self, user_in: SettingUserIn):
        """用户设置保存"""
        await ConfigUtil.set('user', 'defaultAvatar', await UrlUtil.to_relative_url(user_in.default_avatar))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
