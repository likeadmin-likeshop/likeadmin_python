import time
from abc import ABC, abstractmethod
from typing import Union

from fastapi import Request
from sqlalchemy import select

from like.common.enums import SmsEnum
from like.common.sms_captcha import SmsCaptchaManager
from like.dependencies.database import db
from like.front.config import FrontConfig
from like.front.schemas.login import FrontLoginCheckOut, FrontRegisterIn
from like.models.user import user_table, User
from like.utils.redis import RedisUtil
from like.utils.tools import ToolsUtil


class ILoginService(ABC):
    """
    登录管理服务基类(front)
    """

    @abstractmethod
    async def register(self, param: FrontRegisterIn):
        """
        注册
        :return:
        """
        pass

    @abstractmethod
    async def account_login(self, username: str, password: str) -> FrontLoginCheckOut:
        """
        账号登录
        :return:
        """
        pass

    @abstractmethod
    async def mobile_login(self, mobile, code) -> FrontLoginCheckOut:
        """
        手机号登录
        :return:
        """
        pass

    @abstractmethod
    async def mnp_login(self, code, client) -> FrontLoginCheckOut:
        """
        微信小程序登录
        :return:
        """
        pass
    #
    # @abstractmethod
    # async def office_login(self):
    #     """
    #     公众号登录
    #     :return:
    #     """
    #     pass
    #
    # @abstractmethod
    # async def captcha(self):
    #     pass


class LoginService(ILoginService):
    """
    登录管理服务实现类
    """
    table = user_table
    select_columns = [table.c.id, table.c.username, table.c.password, table.c.salt, table.c.mobile, table.c.is_disable]

    def __init__(self, request: Request):
        self.request: Request = request

    async def make_login_token(self, user_id: int, mobile: str = '') -> FrontLoginCheckOut:
        """
        生成登录Token
        :param user_id:
        :param mobile:
        :return:
        """
        token = ToolsUtil.make_token()
        token_valid_time = FrontConfig.token_valid_time
        redis_key = f'{FrontConfig.frontendTokenKey}{token}'
        await RedisUtil.set(redis_key, user_id, token_valid_time)
        return FrontLoginCheckOut(id=user_id, isBindMobile=bool(mobile != ''), token=token)

    async def query_user_by_username(self, username: str) -> Union[User, None]:
        if not username:
            return None
        user = await db.fetch_one(
            select(self.select_columns).select_from(self.table).where(
                self.table.c.is_delete == 0, self.table.c.username == username).limit(1))
        return User(**user) if user else None

    async def query_user_by_mobile(self, mobile: int) -> Union[User, None]:
        if not mobile:
            return None
        user = await db.fetch_one(
            select(self.select_columns).select_from(self.table).where(
                self.table.c.is_delete == 0, self.table.c.mobile == mobile).limit(1))
        return User(**user) if user else None

    async def query_user_by_uid(self, user_id: int) -> Union[User, None]:
        if not user_id:
            return None
        user = await db.fetch_one(
            select(self.select_columns).select_from(self.table).where(
                self.table.c.is_delete == 0, self.table.c.id == user_id).limit(1))
        return User(**user) if user else None

    async def update_user_info(self, user_id: int, ip: str, login_time: int):
        update_dict = {}
        if ip:
            update_dict[self.table.c.last_login_ip.name] = ip
        if login_time:
            update_dict[self.table.c.last_login_time.name] = login_time
        if update_dict:
            return await db.execute(self.table.update()
                                    .where(self.table.c.id == user_id)
                                    .values(**update_dict))

    async def rand_make_sn(self):
        """
        生成随机端用户编号
        :return:
        """
        while True:
            sn = ToolsUtil.random_int(8)
            user = await db.fetch_one(
                select([self.table.c.id]).select_from(self.table).where(
                    self.table.c.is_delete == 0, self.table.c.sn == sn).limit(1))
            if not user:
                break
        return sn

    async def register(self, param: FrontRegisterIn):
        """
        用户注册
        :param param:
        :return:
        """
        user = await self.query_user_by_username(username=param.username)
        assert not user, "账号已存在,换一个吧!"
        sn = await self.rand_make_sn()
        salt = ToolsUtil.random_string(5)
        md5_pwd = ToolsUtil.make_md5(f'{param.password}{salt}')

        user_info = {
            'sn': sn,
            'nickname': '用户%s' % sn,
            'username': param.username,
            'password': md5_pwd,
            'salt': salt,
            'avatar': "/api/static/default_avatar.png",
            'channel': param.client.value,
            'create_time': int(time.time()),
            'update_time': int(time.time())
        }
        return await db.execute(self.table.insert().values(**user_info))

    async def account_login(self, username: str, password: str) -> FrontLoginCheckOut:
        """
        登录管理 账号登录
        :param username:
        :param password:
        :return:
        """
        assert username, 'username参数缺失'
        assert password, 'password参数缺失'
        user = await self.query_user_by_username(username)
        assert user, '账号不存在'

        md5_pwd = ToolsUtil.make_md5(f'{password}{user.salt}')
        assert md5_pwd == user.password, '账号或密码错误'
        assert not user.is_disable, '账号已被禁用'
        ip = self.request.client.host
        await self.update_user_info(user.id, ip=ip, login_time=int(time.time()))
        return await self.make_login_token(user_id=user.id, mobile=user.mobile)

    async def mobile_login(self, mobile, code) -> FrontLoginCheckOut:
        """
        手机号登录
        :return:
        """
        assert mobile, 'mobile参数缺失'
        assert code, 'code参数缺失'
        scene = SmsEnum.LOGIN
        sms_code = await SmsCaptchaManager.get_code(mobile, scene)
        assert sms_code and str(code) == str(sms_code), "验证码错误"

        await SmsCaptchaManager.del_code(mobile, scene)

        user = await self.query_user_by_mobile(mobile)

        assert user, '账号不存在'
        assert not user.is_disable, '账号已被禁用'
        ip = self.request.client.host
        await self.update_user_info(user.id, ip=ip, login_time=int(time.time()))
        return await self.make_login_token(user_id=user.id, mobile=user.mobile)

    async def mnp_login(self, code, client) -> FrontLoginCheckOut:
        """
        小程序登录
        :return:
        """
        pass

    @classmethod
    async def instance(cls, request: Request):
        """实例化"""
        return cls(request=request)
