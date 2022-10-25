import json
from abc import ABC, abstractmethod
from typing import Union, Final

from fastapi import Depends

from like.admin.config import AdminConfig
from like.admin.schemas.system import SystemAuthAdminOut, SystemAuthAdminSelfOut
from like.dependencies.database import db
from like.models import system_auth_admin, system_auth_menu, SystemAuthAdmin
from like.utils.redis import RedisUtil
from .auth_perm import ISystemAuthPermService, SystemAuthPermService


class ISystemAuthAdminService(ABC):
    """系统管理员服务抽象类"""

    @abstractmethod
    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        pass

    @abstractmethod
    async def self(self, admin_id: int) -> SystemAuthAdminSelfOut:
        pass

    @classmethod
    @abstractmethod
    async def cache_admin_user_by_uid(cls, id_: int):
        pass


class SystemAuthAdminService(ISystemAuthAdminService):
    """系统管理员服务实现类"""

    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        """根据账号查找管理员"""
        row = await db.fetch_one(
            system_auth_admin.select().where(system_auth_admin.c.username == username).limit(1))
        return SystemAuthAdmin(**row) if row else None

    async def self(self, admin_id: int) -> SystemAuthAdminSelfOut:
        """当前管理员"""
        # 管理员信息
        sys_admin = await db.fetch_one(
            system_auth_admin.select().where(
                system_auth_admin.c.id == admin_id, system_auth_admin.c.is_delete == 0).limit(1))
        # 角色权限
        auths = []
        if admin_id > 1:
            menu_ids = self.auth_perm_service.select_menus_by_role_id(int(sys_admin.role))
            if menu_ids:
                menus = await db.fetch_all(
                    system_auth_menu.select()
                    .where(system_auth_menu.c.id == menu_ids, system_auth_menu.c.is_disable == 0,
                           system_auth_menu.c.menu_type.in_['C', 'A'])
                    .order_by(system_auth_menu.c.menu_sort, system_auth_menu.c.id))
                if menus:
                    auths.extend((i.perms.strip() for i in menus if i))
            if not auths:
                auths.append('')
        else:
            auths.append('*')
        # TODO: 头像路径处理
        return SystemAuthAdminSelfOut(user=SystemAuthAdminOut(**dict(sys_admin)), permissions=auths)

    @classmethod
    async def cache_admin_user_by_uid(cls, id_: int):
        """缓存管理员"""
        row = await db.fetch_one(
            system_auth_admin.select().where(system_auth_admin.c.id == id_).limit(1))
        await RedisUtil.hmset(f'{AdminConfig.backstage_manage_key}', {f'{row.id}': json.dumps(dict(row))})
        return

    def __init__(self, auth_perm_service: ISystemAuthPermService):
        self.auth_perm_service: Final[ISystemAuthPermService] = auth_perm_service

    @classmethod
    async def instance(cls, auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance)):
        """实例化"""
        return cls(auth_perm_service)
