import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.admin.schemas.system import SystemAuthPostAddIn, SystemAuthPostEditIn, SystemAuthPostOut
from like.dependencies.database import db
from like.models.system import system_auth_post, system_auth_admin


class ISystemAuthPostService(ABC):

    @abstractmethod
    async def fetch_all(self):
        pass

    async def fetch_list(self, code: str = '', name: str = '', is_stop: int = None):
        pass

    @abstractmethod
    async def add(self, post_add_in):
        pass

    @abstractmethod
    async def delete(self, _id):
        pass

    @abstractmethod
    async def edit(self, post_edit_in):
        pass

    @abstractmethod
    async def detail(self, _id):
        pass


class SystemAuthPostService(ISystemAuthPostService):
    select_columns = [system_auth_post.c.id, system_auth_post.c.name, system_auth_post.c.code,
                      system_auth_post.c.remarks,
                      system_auth_post.c.sort, system_auth_post.c.is_stop, system_auth_post.c.create_time,
                      system_auth_post.c.update_time]
    order_by = [system_auth_post.c.sort.desc(), system_auth_post.c.id.desc()]

    async def fetch_all(self):
        post_all = await db.fetch_all(
            select(self.select_columns).where(system_auth_post.c.is_delete == 0).order_by(*self.order_by))
        return pydantic.parse_obj_as(List[SystemAuthPostOut], post_all)

    async def fetch_list(self, code: str = '', name: str = '', is_stop: int = None):
        where = [system_auth_post.c.is_delete == 0]
        if code:
            where.append(system_auth_post.c.code == code)
        if name:
            where.append(system_auth_post.c.name.like('%{0}%'.format(name)))
        if is_stop:
            where.append(system_auth_post.c.is_stop == is_stop)
        query = select(self.select_columns).select_from(system_auth_post).where(*where).order_by(*self.order_by)
        return await paginate(db, query)

    async def add(self, post_add_in: SystemAuthPostAddIn):
        assert not await db.fetch_one(system_auth_post.select().where(
            system_auth_post.c.code == post_add_in.code or system_auth_post.c.name == post_add_in.name,
            system_auth_post.c.is_delete == 0).limit(1)), '该岗位已存在'
        create_post = post_add_in.dict()
        create_post['create_time'] = int(time.time())
        create_post['update_time'] = int(time.time())
        query = system_auth_post.insert().values(**create_post)
        return await db.execute(query)

    async def edit(self, post_edit_in: SystemAuthPostEditIn):
        assert await db.fetch_one(system_auth_post.select().where(
            system_auth_post.c.id == post_edit_in.id,
            system_auth_post.c.is_delete == 0).limit(1)), '岗位不存在'

        assert not await db.fetch_one(system_auth_post.select().where(
            system_auth_post.c.id != post_edit_in.id,
            system_auth_post.c.code == post_edit_in.code or system_auth_post.c.name == post_edit_in.name,
            system_auth_post.c.is_delete == 0).limit(1)), '该岗位已存在'

        edit_post = post_edit_in.dict()
        edit_post['update_time'] = int(time.time())

        return await db.execute(system_auth_post.update()
                                .where(system_auth_post.c.id == post_edit_in.id)
                                .values(**edit_post))

    async def delete(self, _id):
        assert await db.fetch_one(system_auth_post.select().where(
            system_auth_post.c.id == _id,
            system_auth_post.c.is_delete == 0).limit(1)), '岗位不存在'

        assert not await db.fetch_one(system_auth_admin.select().where(
            system_auth_admin.c.post_ids == _id,
            system_auth_admin.c.is_delete == 0).limit(1)), '该岗位已被管理员使用,请先移除'

        return await db.execute(system_auth_post.update()
                                .where(system_auth_post.c.id == _id)
                                .values(is_delete=1, delete_time=int(time.time())))

    async def detail(self, _id):
        post_detail = await db.fetch_one(system_auth_post.select().where(
            system_auth_post.c.id == _id,
            system_auth_post.c.is_delete == 0).limit(1))
        assert post_detail, '岗位不存在'
        return post_detail

    @classmethod
    async def instance(cls):
        return cls()
