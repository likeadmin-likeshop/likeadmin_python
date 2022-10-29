from typing import Final
from abc import ABC, abstractmethod

from sqlalchemy import func, select
from fastapi import Depends

from like.dependencies.database import db
from like.admin.schemas.system import SystemAuthRoleOut
from like.models import system_auth_role, system_auth_admin
from .auth_perm import ISystemAuthPermService, SystemAuthPermService


class ISystemAuthRoleService(ABC):
    """系统角色服务抽象类"""

    @abstractmethod
    async def detail(self, id_: int) -> SystemAuthRoleOut:
        pass


class SystemAuthRoleService(ISystemAuthRoleService):
    """系统角色服务实现类"""

    async def detail(self, id_: int) -> SystemAuthRoleOut:
        """角色详情"""
        role = await db.fetch_one(system_auth_role.select().where(system_auth_role.c.id == id_).limit(1))
        assert role, '角色已不存在!'
        role_dict = dict(role)
        role_dict['member'] = await db.fetch_val(
            select(func.count(system_auth_admin.c.id))
            .where(system_auth_admin.c.role == role.id, system_auth_admin.c.is_delete == 0))
        role_dict['menus'] = await self.auth_perm_service.select_menus_by_role_id(role.id)
        return SystemAuthRoleOut(**role_dict)

    def __init__(self, auth_perm_service: ISystemAuthPermService):
        self.auth_perm_service: Final[ISystemAuthPermService] = auth_perm_service

    @classmethod
    async def instance(cls, auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance)):
        """实例化"""
        return cls(auth_perm_service)
