from abc import ABC, abstractmethod
from typing import Union
import json

from like.admin.config import AdminConfig
from like.dependencies.database import db
from like.models import system_auth_admin, SystemAuthAdmin
from like.utils.redis import RedisUtil


class ISystemAuthAdminService(ABC):

    @abstractmethod
    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        pass

    @classmethod
    @abstractmethod
    async def cache_admin_user_by_uid(cls, id_: int):
        pass


class SystemAuthAdminService(ISystemAuthAdminService):

    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        row = await db.fetch_one(
            system_auth_admin.select().where(system_auth_admin.c.username == username).limit(1))
        return SystemAuthAdmin(**row) if row else None

    @classmethod
    async def cache_admin_user_by_uid(cls, id_: int):
        row = await db.fetch_one(
            system_auth_admin.select().where(system_auth_admin.c.id == id_).limit(1))
        await RedisUtil.hmset(f'{AdminConfig.backstage_manage_key}', {f'{row.id}': json.dumps(dict(row))})
        return

    @classmethod
    async def instance(cls):
        return cls()
