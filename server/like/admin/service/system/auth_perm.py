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
    async def select_menus_by_role_id(cls, role_id: int) -> List[int]:
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
    async def select_menus_by_role_id(cls, role_id: int) -> List[int]:
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
                    system_auth_menu.c.menu_type in ['C', 'A'])) \
                .order_by(system_auth_menu.c.menu_sort, system_auth_menu.c.id)
            menus = [i.perms for i in auth_menus if i.perms]
        await RedisUtil.hset(AdminConfig.backstage_roles_key, str(role_id), ','.join(menus))

    async def batch_save_by_menu_ids(self, role_id: int, menu_ids: str):
        pass

    async def batch_delete_by_role_id(self, role_id: int):
        pass

    async def batch_delete_by_menu_id(self, menu_id: int):
        pass

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
