import logging
import time
from abc import ABC, abstractmethod

from fastapi import Request, Depends

from like.admin.config import AdminConfig
from like.dependencies.database import db
from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.models import system_auth_admin
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
            # TODO: record
            raise
        if sys_admin.is_disable:
            # TODO: record
            raise
        md5_pwd = ToolsUtil.make_md5(f'{login_in.password}{sys_admin.salt}')
        if sys_admin.password != md5_pwd:
            # TODO: record
            raise
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

            # TODO: record
            return response
        except Exception as e:
            # TODO: record
            raise AppException(HttpResp.FAILED, echo_exc=True)

    async def logout(self, logout_in: SystemLogoutIn):
        await RedisUtil.delete(f'{AdminConfig.backstage_token_key}{logout_in.token}')

    def __init__(self, request: Request, auth_service: ISystemAuthAdminService):
        self.request = request
        self.auth_admin_service = auth_service

    @classmethod
    async def instance(cls, request: Request,
                       auth_admin_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
        return cls(request, auth_admin_service)
