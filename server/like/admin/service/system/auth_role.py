import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi import Depends
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import func, select

from like.admin.config import AdminConfig
from like.admin.schemas.system import (
    SystemAuthRoleCreateIn, SystemAuthRoleEditIn, SystemAuthRoleOut, SystemAuthRoleDetailOut)
from like.dependencies.database import db
from like.models import system_auth_role, system_auth_admin
from like.utils.redis import RedisUtil
from .auth_perm import ISystemAuthPermService, SystemAuthPermService


class ISystemAuthRoleService(ABC):
    """系统角色服务抽象类"""

    @abstractmethod
    async def all(self) -> List[SystemAuthRoleOut]:
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
        """角色列表"""
        query = system_auth_role.select() \
            .order_by(system_auth_role.c.sort.desc(), system_auth_role.c.id.desc())
        pager = await paginate(db, query)
        for obj in pager.lists:
            obj.member = await self.get_member_cnt(obj.id)
        return pager

    async def get_member_cnt(self, role_id: int):
        """根据角色ID获取成员数量"""
        return await db.fetch_val(
            select(func.count(system_auth_admin.c.id))
            .where(system_auth_admin.c.role == role_id, system_auth_admin.c.is_delete == 0))

    async def detail(self, id_: int) -> SystemAuthRoleDetailOut:
        """角色详情"""
        role = await db.fetch_one(system_auth_role.select().where(system_auth_role.c.id == id_).limit(1))
        assert role, '角色已不存在!'
        role_id = role.id
        role_dict = dict(role)
        role_dict['member'] = await self.get_member_cnt(role_id)
        role_dict['menus'] = await self.auth_perm_service.select_menu_ids_by_role_id([role_id])
        return SystemAuthRoleDetailOut(**role_dict)

    @db.transaction()
    async def add(self, create_in: SystemAuthRoleCreateIn):
        """新增角色"""
        assert not await db.fetch_one(
            system_auth_role.select().where(system_auth_role.c.name == create_in.name.strip())
            .limit(1)), '角色名称已存在!'
        role_dict = create_in.dict()
        role_dict['name'] = create_in.name.strip()
        role_dict['create_time'] = int(time.time())
        role_dict['update_time'] = int(time.time())
        del role_dict['menu_ids']
        result = await db.execute(system_auth_role.insert().values(role_dict))
        await self.auth_perm_service.batch_save_by_menu_ids(result, create_in.menu_ids)

    @db.transaction()
    async def edit(self, edit_in: SystemAuthRoleEditIn):
        """编辑角色"""
        assert await db.fetch_one(
            system_auth_role.select().where(system_auth_role.c.id == edit_in.id)
            .limit(1)), '角色已不存在!'
        assert not await db.fetch_one(
            system_auth_role.select()
            .where(system_auth_role.c.id != edit_in.id,
                   system_auth_role.c.name == edit_in.name.strip())
            .limit(1)), '角色名称已存在!'
        role_dict = edit_in.dict()
        role_dict['name'] = edit_in.name.strip()
        role_dict['update_time'] = int(time.time())
        del role_dict['menu_ids']
        await db.execute(
            system_auth_role.update().where(system_auth_role.c.id == edit_in.id).values(**role_dict))
        await self.auth_perm_service.batch_delete_by_role_id(edit_in.id)
        await self.auth_perm_service.batch_save_by_menu_ids(edit_in.id, edit_in.menu_ids)
        await self.auth_perm_service.cache_role_menus_by_role_id(edit_in.id)

    @db.transaction()
    async def delete(self, id_: int):
        """删除角色"""
        assert await db.fetch_one(
            system_auth_role.select().where(system_auth_role.c.id == id_)
            .limit(1)), '角色已不存在!'
        assert not await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.role == id_, system_auth_admin.c.is_delete == 0)
            .limit(1)), '角色已被管理员使用,请先移除'
        await db.execute(system_auth_role.delete().where(system_auth_role.c.id == id_))
        await self.auth_perm_service.batch_delete_by_role_id(id_)
        await RedisUtil.hdel(AdminConfig.backstage_roles_key, str(id_))

    def __init__(self, auth_perm_service: ISystemAuthPermService):
        self.auth_perm_service: ISystemAuthPermService = auth_perm_service

    @classmethod
    async def instance(cls, auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance)):
        """实例化"""
        return cls(auth_perm_service)
