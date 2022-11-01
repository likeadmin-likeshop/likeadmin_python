import uuid
from abc import ABC, abstractmethod
from typing import List

from like.admin.config import AdminConfig
from like.dependencies.database import db
from like.models import system_auth_menu, system_auth_perm, system_auth_role
from like.utils.redis import RedisUtil


class ISystemAuthPermService(ABC):
    """系统权限服务抽象类"""

    @classmethod
    @abstractmethod
    async def select_menu_ids_by_role_id(cls, role_id: int) -> List[int]:
        pass

    @classmethod
    @abstractmethod
    async def cache_role_menus_by_role_id(cls, role_id: int):
        pass

    @abstractmethod
    async def batch_save_by_menu_ids(self, role_id: int, menu_ids: str):
        pass

    @abstractmethod
    async def batch_delete_by_role_id(self, role_id: int):
        pass

    @abstractmethod
    async def batch_delete_by_menu_id(self, menu_id: int):
        pass


class SystemAuthPermService(ISystemAuthPermService):
    """系统权限服务实现类"""

    @classmethod
    async def select_menu_ids_by_role_id(cls, role_id: int) -> List[int]:
        """根据角色ID获取菜单ID"""
        role = await db.fetch_one(
            system_auth_role.select()
            .where(system_auth_role.c.id == role_id, system_auth_role.c.is_disable == 0).limit(1))
        if not role:
            return []
        perms = await db.fetch_all(system_auth_perm.select().where(system_auth_perm.c.role_id == role_id))
        return [i.menu_id for i in perms]

    @classmethod
    async def cache_role_menus_by_role_id(cls, role_id: int):
        """缓存角色菜单"""
        auth_perms = await db.fetch_all(
            system_auth_perm.select().where(system_auth_perm.c.role_id == role_id))
        menu_ids = [i.menu_id for i in auth_perms]
        menus = []
        if menu_ids:
            auth_menus = await db.fetch_all(
                system_auth_menu.select().where(
                    system_auth_menu.c.is_disable == 0,
                    system_auth_menu.c.id in menu_ids,
                    system_auth_menu.c.menu_type in ['C', 'A'])
                .order_by(system_auth_menu.c.menu_sort, system_auth_menu.c.id))
            menus = [i.perms for i in auth_menus if i.perms]
        await RedisUtil.hset(AdminConfig.backstage_roles_key, str(role_id), ','.join(menus))

    async def batch_save_by_menu_ids(self, role_id: int, menu_ids: str):
        """批量写入角色菜单"""
        if menu_ids:
            perms = []
            for menu_id in menu_ids.split(','):
                perms.append({'id': uuid.uuid4().hex, 'role_id': role_id, 'menu_id': int(menu_id)})
            perm_ins = system_auth_perm.insert().values(perms)
            await db.execute(perm_ins)

    async def batch_delete_by_role_id(self, role_id: int):
        """批量删除角色菜单(根据角色ID)"""
        await db.execute(system_auth_perm.delete().where(system_auth_perm.c.role_id == role_id))

    async def batch_delete_by_menu_id(self, menu_id: int):
        """批量删除角色菜单(根据菜单ID)"""
        await db.execute(system_auth_perm.delete().where(system_auth_perm.c.menu_id == menu_id))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
