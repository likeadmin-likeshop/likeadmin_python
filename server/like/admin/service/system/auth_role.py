from abc import ABC, abstractmethod
from typing import Final, List

import pydantic
from fastapi import Depends
from fastapi_pagination.bases import AbstractPage
from sqlalchemy import func, select

from like.admin.schemas.system import (
    SystemAuthRoleCreateIn, SystemAuthRoleEditIn, SystemAuthRoleOut, SystemAuthRoleDetailOut)
from like.dependencies.database import db
from like.models import system_auth_role, system_auth_admin
from .auth_perm import ISystemAuthPermService, SystemAuthPermService


class ISystemAuthRoleService(ABC):
    """系统角色服务抽象类"""

    @abstractmethod
    async def all(self) -> AbstractPage[SystemAuthRoleOut]:
        pass

    @abstractmethod
    async def list(self) -> AbstractPage[SystemAuthRoleDetailOut]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> SystemAuthRoleDetailOut:
        pass

    @abstractmethod
    async def add(self, create_in: SystemAuthRoleCreateIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: SystemAuthRoleEditIn):
        pass

    @abstractmethod
    async def delete(self, id_: int):
        pass


class SystemAuthRoleService(ISystemAuthRoleService):
    """系统角色服务实现类"""

    async def all(self) -> List[SystemAuthRoleOut]:
        """角色所有"""
        roles = await db.fetch_all(
            system_auth_role.select()
            .order_by(system_auth_role.c.sort.desc(), system_auth_role.c.id.desc()))
        return pydantic.parse_obj_as(List[SystemAuthRoleOut], roles)

    async def list(self) -> AbstractPage[SystemAuthRoleDetailOut]:
        pass

    async def detail(self, id_: int) -> SystemAuthRoleDetailOut:
        """角色详情"""
        role = await db.fetch_one(system_auth_role.select().where(system_auth_role.c.id == id_).limit(1))
        assert role, '角色已不存在!'
        role_dict = dict(role)
        role_dict['member'] = await db.fetch_val(
            select(func.count(system_auth_admin.c.id))
            .where(system_auth_admin.c.role == role.id, system_auth_admin.c.is_delete == 0))
        role_dict['menus'] = await self.auth_perm_service.select_menus_by_role_id(role.id)
        return SystemAuthRoleDetailOut(**role_dict)

    async def add(self, create_in: SystemAuthRoleCreateIn):
        pass

    async def edit(self, edit_in: SystemAuthRoleEditIn):
        pass

    async def delete(self, id_: int):
        pass

    def __init__(self, auth_perm_service: ISystemAuthPermService):
        self.auth_perm_service: Final[ISystemAuthPermService] = auth_perm_service

    @classmethod
    async def instance(cls, auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance)):
        """实例化"""
        return cls(auth_perm_service)
