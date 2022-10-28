from abc import ABC, abstractmethod

from fastapi_pagination.ext.databases import paginate

from like.dependencies.database import db
from like.models.system import system_auth_post


class ISystemAuthPostService(ABC):

    @abstractmethod
    async def fetch_all(self):
        pass

    async def fetch_list(self, code: str = '', name: str = '', is_stop: int = None):
        pass


class SystemAuthPostService(ISystemAuthPostService):

    async def fetch_all(self):
        return await db.fetch_all(system_auth_post.select())

    async def fetch_list(self, code: str = '', name: str = '', is_stop: int = None):
        where = []
        if code:
            where.append(system_auth_post.c.code == code)
        if name:
            where.append(system_auth_post.c.name == name)
        if is_stop:
            where.append(system_auth_post.c.is_stop == is_stop)
        query = system_auth_post.select().where(*where)
        return await paginate(db, query)

    @classmethod
    async def instance(cls):
        return cls()
