from abc import ABC, abstractmethod

from like.common.enums import LoginClientEnum, get_sex
from like.config import get_settings
from like.dependencies.database import db
from like.front.schemas.user import UserCenterOut, UserInfoOut
from like.models import user_table, user_auth
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IUserService(ABC):
    """用户服务抽象类"""

    @abstractmethod
    async def center(self, user_id: int) -> UserCenterOut:
        pass

    @abstractmethod
    async def info(self, user_id: int) -> UserInfoOut:
        pass

    @abstractmethod
    async def edit(self):
        pass

    @abstractmethod
    async def change_pwd(self):
        pass

    @abstractmethod
    async def bind_mobile(self):
        pass

    @abstractmethod
    async def mnp_mobile(self):
        pass


class UserService(IUserService):
    """用户服务实现类"""

    async def center(self, user_id: int) -> UserCenterOut:
        """个人中心"""
        obj = await db.fetch_one(user_table.select().where(user_table.c.id == user_id).limit(1))
        res = UserCenterOut.from_orm(obj)
        if res.avatar:
            res.avatar = await UrlUtil.to_absolute_url(res.avatar)
        else:
            res.avatar = await UrlUtil.to_absolute_url(await ConfigUtil.get_val('user', 'defaultAvatar', ''))
        return res

    async def info(self, user_id: int) -> UserInfoOut:
        """个人信息"""
        obj = await db.fetch_one(user_table.select().where(user_table.c.id == user_id).limit(1))
        auth = await db.fetch_one(
            user_auth.select().where(user_auth.c.user_id == user_id, user_auth.c.client == LoginClientEnum.MNP.value)
            .limit(1))
        res = UserInfoOut.from_orm(obj)
        res.isPassword = True if obj.password else False
        res.isBindMnp = True if auth else False
        res.version = get_settings().version
        res.sex = get_sex(obj.sex)
        if res.avatar:
            res.avatar = await UrlUtil.to_absolute_url(res.avatar)
        else:
            res.avatar = await UrlUtil.to_absolute_url(await ConfigUtil.get_val('user', 'defaultAvatar', ''))
        return res

    async def edit(self):
        pass

    async def change_pwd(self):
        pass

    async def bind_mobile(self):
        pass

    async def mnp_mobile(self):
        pass

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
