import time
from abc import ABC, abstractmethod
from typing import List, Union

import pydantic
from fastapi import Depends, Request

from like.admin.config import AdminConfig
from like.admin.schemas.system import (
    SystemAuthMenuCreateIn, SystemAuthMenuEditIn, SystemAuthMenuOut)
from like.dependencies.database import db
from like.models import system_auth_menu
from like.utils.array import ArrayUtil
from like.utils.redis import RedisUtil
from .auth_perm import ISystemAuthPermService, SystemAuthPermService


class ISystemAuthMenuService(ABC):
    """系统菜单服务抽象类"""

    @abstractmethod
    async def select_menu_by_role_id(self, role_id) -> List[Union[SystemAuthMenuOut, dict]]:
        pass

    @abstractmethod
    async def list(self) -> List[Union[SystemAuthMenuOut, dict]]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> Union[SystemAuthMenuOut, dict]:
        pass

    @abstractmethod
    async def add(self, create_in: SystemAuthMenuCreateIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: SystemAuthMenuEditIn):
        pass

    @abstractmethod
    async def delete(self, id_: int):
        pass


class SystemAuthMenuService(ISystemAuthMenuService):
    """系统菜单服务实现类"""

    async def select_menu_by_role_id(self, role_id) -> List[Union[SystemAuthMenuOut, dict]]:
        """根据角色ID获取菜单"""
        admin_id = self.request.state.admin_id
        menu_ids = await self.auth_perm_service.select_menu_ids_by_role_id(role_id) or [0]
        where = [system_auth_menu.c.menu_type.in_(('M', 'C')),
                 system_auth_menu.c.is_disable == 0]
        if admin_id != 1:
            where.append(system_auth_menu.c.id.in_(menu_ids))
        menus = await db.fetch_all(
            system_auth_menu.select().where(*where)
            .order_by(system_auth_menu.c.menu_sort.desc(), system_auth_menu.c.id))
        return ArrayUtil.list_to_tree(
            [i.dict(exclude_none=True) for i in pydantic.parse_obj_as(List[SystemAuthMenuOut], menus)],
            'id', 'pid', 'children')

    async def list(self) -> List[Union[SystemAuthMenuOut, dict]]:
        """菜单列表"""
        menus = await db.fetch_all(
            system_auth_menu.select()
            .order_by(system_auth_menu.c.menu_sort.desc(), system_auth_menu.c.id))
        return ArrayUtil.list_to_tree(
            [i.dict(exclude_none=True) for i in pydantic.parse_obj_as(List[SystemAuthMenuOut], menus)],
            'id', 'pid', 'children')

    async def detail(self, id_: int) -> Union[SystemAuthMenuOut, dict]:
        """菜单详情"""
        menu = await db.fetch_one(
            system_auth_menu.select().where(system_auth_menu.c.id == id_).limit(1))
        assert menu, '菜单已不存在!'
        return SystemAuthMenuOut.from_orm(menu).dict(exclude_none=True)

    async def add(self, create_in: SystemAuthMenuCreateIn):
        """新增菜单"""
        create_dict = create_in.dict()
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(system_auth_menu.insert().values(**create_dict))
        await RedisUtil.delete(AdminConfig.backstage_roles_key)

    async def edit(self, edit_in: SystemAuthMenuEditIn):
        """编辑菜单"""
        assert await db.fetch_one(
            system_auth_menu.select().where(system_auth_menu.c.id == edit_in.id).limit(1)), '菜单已不存在!'
        edit_dict = edit_in.dict()
        edit_dict['update_time'] = int(time.time())
        await db.execute(system_auth_menu.update().where(system_auth_menu.c.id == edit_in.id).values(**edit_dict))
        await RedisUtil.delete(AdminConfig.backstage_roles_key)

    async def delete(self, id_: int):
        """删除菜单"""
        assert await db.fetch_one(
            system_auth_menu.select().where(system_auth_menu.c.id == id_).limit(1)), '菜单已不存在!'
        assert not await db.fetch_one(
            system_auth_menu.select().where(system_auth_menu.c.pid == id_)), '请先删除子菜单再操作！'
        await db.execute(system_auth_menu.delete().where(system_auth_menu.c.id == id_))
        await self.auth_perm_service.batch_delete_by_menu_id(id_)
        await RedisUtil.delete(AdminConfig.backstage_roles_key)

    def __init__(self, request: Request, auth_perm_service: ISystemAuthPermService):
        self.request: Request = request
        self.auth_perm_service: ISystemAuthPermService = auth_perm_service

    @classmethod
    async def instance(cls, request: Request,
                       auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance)):
        """实例化"""
        return cls(request, auth_perm_service)
