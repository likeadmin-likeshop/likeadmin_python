from abc import ABC, abstractmethod
from typing import Union

from fastapi_cache.decorator import cache

from like.admin.config import AdminConfig
from like.dependencies.database import db
from like.models import system_auth_admin, SystemAuthAdmin


class ISystemAuthAdminService(ABC):

    @abstractmethod
    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        pass

    @abstractmethod
    async def cache_admin_user_by_uid(self, id_: int) -> Union[SystemAuthAdmin, None]:
        pass


class SystemAuthAdminService(ISystemAuthAdminService):

    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        row = await db.fetch_one(
            system_auth_admin.select().where(system_auth_admin.c.username == username).limit(1))
        return SystemAuthAdmin(**row) if row else None

    async def cache_admin_user_by_uid(self, id_: int) -> Union[SystemAuthAdmin, None]:
        @cache()
        async def cache_admin_user(_key: int):
            return await db.fetch_one(
                system_auth_admin.select().where(system_auth_admin.c.id == id_).limit(1))

        row = await cache_admin_user(f'{AdminConfig.backstage_manage_key}')
        return SystemAuthAdmin(**row) if row else None

    @classmethod
    async def instance(cls):
        return cls()
