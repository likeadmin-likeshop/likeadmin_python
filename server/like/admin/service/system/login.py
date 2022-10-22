import logging
import time
from abc import ABC, abstractmethod

import user_agents
from fastapi import Request, Depends

from like.admin.config import AdminConfig
from like.dependencies.database import db
from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.models import system_auth_admin, system_log_login
from like.utils.redis import RedisUtil
from like.utils.tools import ToolsUtil
from .auth_admin import ISystemAuthAdminService, SystemAuthAdminService
from ...schemas.system import SystemLoginIn, SystemLoginOut, SystemLogoutIn


class ISystemLoginService(ABC):

    @abstractmethod
    async def login(self, login_in: SystemLoginIn) -> SystemLoginOut:
        pass

    @abstractmethod
    async def logout(self, logout_in: SystemLogoutIn):
        pass


class SystemLoginService(ISystemLoginService):
    auth_admin_service: ISystemAuthAdminService

    async def login(self, login_in: SystemLoginIn) -> SystemLoginOut:
        sys_admin = await self.auth_admin_service.find_by_username(login_in.username)
        if not sys_admin or sys_admin.is_delete:
            await self.record_login_log(0, login_in.username, HttpResp.LOGIN_ACCOUNT_ERROR.msg)
            raise AppException(HttpResp.LOGIN_ACCOUNT_ERROR)
        if sys_admin.is_disable:
            await self.record_login_log(sys_admin.id, sys_admin.username, HttpResp.LOGIN_DISABLE_ERROR.msg)
            raise AppException(HttpResp.LOGIN_DISABLE_ERROR)
        md5_pwd = ToolsUtil.make_md5(f'{login_in.password}{sys_admin.salt}')
        if sys_admin.password != md5_pwd:
            await self.record_login_log(sys_admin.id, sys_admin.username, HttpResp.LOGIN_ACCOUNT_ERROR.msg)
            raise AppException(HttpResp.LOGIN_ACCOUNT_ERROR)
        try:
            token = ToolsUtil.make_token()
            if not sys_admin.is_multipoint:
                sys_admin_set_key = f'{AdminConfig.backstage_token_set}{sys_admin.id}'
                ts = await RedisUtil.sget(sys_admin_set_key)
                if ts:
                    await RedisUtil.delete(*(f'{AdminConfig.backstage_token_key}{t}' for t in ts))
                await RedisUtil.delete(sys_admin_set_key)
                await RedisUtil.sset(sys_admin_set_key, token)

            await RedisUtil.set(f'{AdminConfig.backstage_token_key}{token}', sys_admin.id, 7200)
            await self.auth_admin_service.cache_admin_user_by_uid(sys_admin.id)

            response = SystemLoginOut(token=token)
            row_update = system_auth_admin.update().where(system_auth_admin.c.id == sys_admin.id) \
                .values(last_login_ip=self.request.client.host, last_login_time=int(time.time()))
            await db.execute(row_update)

            await self.record_login_log(sys_admin.id, sys_admin.username)
            return response
        except Exception as e:
            err_msg = str(e)
            await self.record_login_log(sys_admin.id, sys_admin.username, err_msg if err_msg else '未知错误')
            raise AppException(HttpResp.FAILED, echo_exc=True)

    async def logout(self, logout_in: SystemLogoutIn):
        await RedisUtil.delete(f'{AdminConfig.backstage_token_key}{logout_in.token}')

    async def record_login_log(self, admin_id: int, username: str, error: str = ''):
        ua = user_agents.parse(self.request.headers.get('user-agent', ''))
        try:
            row = system_log_login.insert().values(
                admin_id=admin_id, username=username, ip=self.request.client.host,
                os=ua.os.family, browser=ua.browser.family, status=0 if error else 1, create_time=int(time.time()))
            await db.execute(row)
        except Exception as e:
            logging.error('记录登录日志异常 %s', str(e))

    def __init__(self, request: Request, auth_service: ISystemAuthAdminService):
        self.request = request
        self.auth_admin_service = auth_service

    @classmethod
    async def instance(cls, request: Request,
                       auth_admin_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
        return cls(request, auth_admin_service)
