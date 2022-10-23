from abc import ABC, abstractmethod

from like.admin.config import AdminConfig
from like.dependencies.database import db
from like.models import system_auth_menu, system_auth_perm
from like.utils.redis import RedisUtil


class ISystemAuthPermService(ABC):
    """系统权限服务抽象类"""

    @classmethod
    @abstractmethod
    async def cache_role_menus_by_role_id(cls, id_: int):
        pass


class SystemAuthPermService(ISystemAuthPermService):
    """系统权限服务实现类"""

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

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
