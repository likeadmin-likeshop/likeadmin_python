from abc import ABC, abstractmethod

from like.admin.schemas.setting import SettingLoginIn
from like.utils.config import ConfigUtil


class ISettingLoginService(ABC):
    """登录设置服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, login_in: SettingLoginIn):
        pass


class SettingLoginService(ISettingLoginService):
    """登录设置服务实现类"""

    async def detail(self) -> dict:
        """登录设置详情"""
        config = await ConfigUtil.get('login')
        return {
            'loginWay': [int(i) for i in config.get('loginWay', '').split(',') if i.isdigit()],  # 登录方式
            'forceBindMobile': int(config.get('forceBindMobile')) if config.get('forceBindMobile') else 0,  # 强制绑定手机
            'openAgreement': int(config.get('openAgreement')) if config.get('openAgreement') else 0,  # 是否开启协议
            'openOtherAuth': int(config.get('openOtherAuth')) if config.get('openOtherAuth') else 0,  # 第三方的登录
            'autoLoginAuth': [int(i) for i in config.get('autoLoginAuth', '').split(',') if i.isdigit()],  # 自动登录授权
        }

    async def save(self, login_in: SettingLoginIn):
        """登录设置保存"""
        await ConfigUtil.set('login', 'loginWay', login_in.login_way)
        await ConfigUtil.set('login', 'forceBindMobile', str(login_in.force_bind_mobile))
        await ConfigUtil.set('login', 'openAgreement', str(login_in.open_agreement))
        await ConfigUtil.set('login', 'openOtherAuth', str(login_in.open_other_auth))
        await ConfigUtil.set('login', 'autoLoginAuth', login_in.auto_login_auth)

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
