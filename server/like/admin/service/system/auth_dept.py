import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from sqlalchemy import select

from like.admin.schemas.system import SystemAuthDeptAddIn, SystemAuthDeptEditIn, SystemAuthDeptOut
from like.dependencies.database import db
from like.models import system_auth_dept
from like.utils.array import ArrayUtil


class ISystemAuthDeptService(ABC):

    @abstractmethod
    async def fetch_all(self):
        pass

    async def fetch_list(self, name: str = '', is_stop: int = None):
        pass

    @abstractmethod
    async def add(self, dept_add_in):
        pass

    async def delete(self, dept_id):
        pass

    async def edit(self, dept_edit_in):
        pass

    async def detail(self, dept_id):
        pass


class SystemAuthDeptService():
    select_columns = [system_auth_dept.c.id, system_auth_dept.c.pid, system_auth_dept.c.name,
                      system_auth_dept.c.duty, system_auth_dept.c.mobile, system_auth_dept.c.sort,
                      system_auth_dept.c.is_stop, system_auth_dept.c.create_time,
                      system_auth_dept.c.update_time]
    order_by = [system_auth_dept.c.sort.desc(), system_auth_dept.c.id.desc()]

    async def fetch_all(self):
        dept_all = await db.fetch_all(
            select(self.select_columns).where(system_auth_dept.c.pid >= 0, system_auth_dept.c.is_delete == 0).order_by(
                *self.order_by))
        return [SystemAuthDeptOut(**dept) for dept in dept_all]

    async def fetch_list(self, name: str = '', is_stop: int = None):
        where = [system_auth_dept.c.is_delete == 0]
        if name:
            where.append(system_auth_dept.c.name == name)
        if is_stop:
            where.append(system_auth_dept.c.is_stop == is_stop)
        depts = await db.fetch_all(
            select(self.select_columns).select_from(system_auth_dept).where(*where).order_by(*self.order_by))
        return ArrayUtil.list_to_tree(
            [i.dict(exclude_none=True) for i in pydantic.parse_obj_as(List[SystemAuthDeptOut], depts)],
            'id', 'pid', 'children')

    async def add(self, dept_add_in: SystemAuthDeptAddIn):
        if dept_add_in.pid == 0 :
            assert not await db.fetch_one(
                system_auth_dept.select([system_auth_dept.c.id, system_auth_dept.c.pid, system_auth_dept.c.name]).where(
                    system_auth_dept.c.pid == 0, system_auth_dept.c.is_delete == 0)), "顶级部门只允许有一个"
        create_dept = dept_add_in.dict()
        create_dept['create_time'] = int(time.time())
        create_dept['update_time'] = int(time.time())
        query = system_auth_dept.insert().values(**create_dept)
        return await db.execute(query)

    async def edit(self, dept_edit_in: SystemAuthDeptEditIn):
        edit_dept = await db.fetch_one(system_auth_dept.select().where
                                       (system_auth_dept.c.id == dept_edit_in.id,
                                        system_auth_dept.c.is_delete == 0).limit(1))
        assert edit_dept, '部门不存在'

        assert not (edit_dept.pid == 0 and dept_edit_in.pid > 0), "顶级部门不能修改上级"
        assert not (edit_dept.pid == dept_edit_in.pid), "上级部门不能是自己"

        edit_post = dept_edit_in.dict()
        edit_post['update_time'] = int(time.time())
        return await db.execute(system_auth_dept.update()
                                .where(system_auth_dept.c.id == dept_edit_in.id)
                                .values(**edit_post))

    async def delete(self, dept_id):
        del_dept = await  db.fetch_one(system_auth_dept.select().where
                                       (system_auth_dept.c.id == dept_id,
                                        system_auth_dept.c.is_delete == 0).limit(1))
        assert del_dept, '部门不存在'
        assert del_dept.pid != 0, '顶级部门不能删除'

        del_dept_child = await db.fetch_one(system_auth_dept.select().where
                                            (system_auth_dept.c.pid == dept_id,
                                             system_auth_dept.c.is_delete == 0).limit(1))

        assert not del_dept_child, '请先删除子级部门'

        return await db.execute(system_auth_dept.update()
                                .where(system_auth_dept.c.id == dept_id)
                                .values(is_delete=1, delete_time=int(time.time())))

    async def detail(self, dept_id):
        post_detail = await db.fetch_one(system_auth_dept.select().where(
            system_auth_dept.c.id == dept_id,
            system_auth_dept.c.is_delete == 0).limit(1))
        assert post_detail, '部门已不存在'
        return post_detail

    @classmethod
    async def instance(cls):
        return cls()
