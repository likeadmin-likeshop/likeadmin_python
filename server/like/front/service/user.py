import time
from abc import ABC, abstractmethod

from like.common.enums import LoginClientEnum, get_sex, NoticeEnum
from like.config import get_settings
from like.dependencies.database import db
from like.exceptions.base import AppException
from like.front.schemas.user import UserCenterOut, UserInfoOut, UserEditIn, UserChangePwdIn, UserBindMobileIn
from like.http_base import HttpResp
from like.models import user_table, user_auth_table
from like.utils.config import ConfigUtil
from like.utils.redis import RedisUtil
from like.utils.tools import ToolsUtil
from like.utils.urls import UrlUtil
from like.utils.wechat import WeChatUtil


class IUserService(ABC):
    """用户服务抽象类"""

    @abstractmethod
    async def center(self, user_id: int) -> UserCenterOut:
        pass

    @abstractmethod
    async def info(self, user_id: int) -> UserInfoOut:
        pass

    @abstractmethod
    async def edit(self, user_id: int, edit_in: UserEditIn):
        pass

    @abstractmethod
    async def change_pwd(self, user_id: int, change_in: UserChangePwdIn):
        pass

    @abstractmethod
    async def bind_mobile(self, user_id: int, bind_in: UserBindMobileIn):
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
            user_auth_table.select().where(user_auth_table.c.user_id == user_id,
                                           user_auth_table.c.client == LoginClientEnum.MNP.value)
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

    async def edit(self, user_id: int, edit_in: UserEditIn):
        """编辑信息"""
        field, value = edit_in.field.strip(), edit_in.value.strip()
        update_dict = {'update_time': int(time.time())}
        if field == 'avatar':
            update_dict['avatar'] = await UrlUtil.to_relative_url(value)
            await db.execute(user_table.update().where(user_table.c.id == user_id).values(**update_dict))
        elif field == 'username':
            obj = await db.fetch_one(
                user_table.select().where(user_table.c.username == value, user_table.c.is_delete == 0).limit(1))
            if obj and obj.id != user_id:
                raise AppException(HttpResp.FAILED, msg='账号已被使用!')
            if obj and obj.username == value:
                raise AppException(HttpResp.FAILED, msg='新账号与旧账号一致,修改失败!')
            update_dict['username'] = value
            await db.execute(user_table.update().where(user_table.c.id == user_id).values(**update_dict))
        elif field == 'nickname':
            update_dict['nickname'] = value
            await db.execute(user_table.update().where(user_table.c.id == user_id).values(**update_dict))
        elif field == 'sex':
            update_dict['sex'] = int(value) if value.isdigit() else 0
            await db.execute(user_table.update().where(user_table.c.id == user_id).values(**update_dict))
        else:
            raise AppException(HttpResp.FAILED, msg='不被支持的类型')

    async def change_pwd(self, user_id: int, change_in: UserChangePwdIn):
        """修改密码"""
        obj = await db.fetch_one(
            user_table.select().where(user_table.c.id == user_id, user_table.c.is_delete == 0).limit(1))
        assert obj, '用户不存在'
        if obj.password:
            assert change_in.old_password, 'oldPassword参数缺失'
            old_pwd = ToolsUtil.make_md5(change_in.old_password.strip() + obj.salt)
            if old_pwd != obj.password:
                raise AppException(HttpResp.FAILED, msg='原密码不正确!')
        salt = ToolsUtil.random_string(5)
        pwd = ToolsUtil.make_md5(change_in.password.strip() + salt)
        await db.execute(user_table.update().where(user_table.c.id == user_id).values(
            password=pwd, salt=salt, update_time=int(time.time())))

    async def bind_mobile(self, user_id: int, bind_in: UserBindMobileIn):
        """绑定手机"""
        type_code = NoticeEnum.SMS_BIND_MOBILE_CODE.value \
            if bind_in.type == 'bind' else NoticeEnum.SMS_CHANGE_MOBILE_CODE.value
        sms_code = await RedisUtil.get(f'{get_settings().redis_sms_code}{type_code}:{bind_in.mobile}')
        if not (sms_code and sms_code == bind_in.code.lower()):
            raise AppException(HttpResp.FAILED, msg='验证码错误!')
        obj = await db.fetch_one(
            user_table.select().where(user_table.c.mobile == bind_in.mobile, user_table.c.is_delete == 0).limit(1))
        if obj and obj.id == user_id:
            raise AppException(HttpResp.FAILED, msg='手机号已被其它账号绑定!')
        await db.execute(user_table.update().where(user_table.c.id == user_id).values(
            mobile=bind_in.mobile, update_time=int(time.time())))

    async def mnp_mobile(self, user_id: int, code: str):
        """微信手机号"""
        client = await WeChatUtil.mnp()
        try:
            data = client._post(
                'wxa/business/getuserphonenumber',
                data={'code': code}
            )
        except Exception as e:
            raise AppException(HttpResp.FAILED, msg=str(e))
        phone_info = data.get('phone_info', {})
        mobile = phone_info.get('phoneNumber', '')
        await db.execute(user_table.update().where(user_table.c.id == user_id).values(
            mobile=mobile, update_time=int(time.time())))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
