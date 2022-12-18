"""
字典管理
"""
import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.admin.schemas.setting import SettingDictTypeOut, SettingDictTypeListIn, SettingDictTypeAddIn, \
    SettingDictTypeEditIn, SettingDictTypeDeleteIn
from like.dependencies.database import db
from like.models.setting import settings_dict_type


class ISettingDictTypeService(ABC):

    @abstractmethod
    async def list(self, list_in: SettingDictTypeListIn) -> AbstractPage[SettingDictTypeOut]:
        pass

    @abstractmethod
    async def all(self) -> List[SettingDictTypeOut]:
        pass

    @abstractmethod
    async def detail(self, _id: int) -> SettingDictTypeOut:
        pass

    @abstractmethod
    async def add(self, add_in: SettingDictTypeAddIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: SettingDictTypeEditIn):
        pass

    @abstractmethod
    async def delete(self, delete_in: SettingDictTypeDeleteIn):
        pass


class ISettingDictDataService(ABC):

    @abstractmethod
    async def list(self, list_in: SettingDictTypeListIn) -> AbstractPage[SettingDictTypeOut]:
        pass

    @abstractmethod
    async def all(self) -> List[SettingDictTypeOut]:
        pass

    @abstractmethod
    async def detail(self, _id: int) -> SettingDictTypeOut:
        pass

    @abstractmethod
    async def add(self, add_in: SettingDictTypeAddIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: SettingDictTypeEditIn):
        pass

    @abstractmethod
    async def delete(self, delete_in: SettingDictTypeDeleteIn):
        pass


class SettingDictTypeService(ISettingDictTypeService):
    select_columns = [settings_dict_type.c.id, settings_dict_type.c.dict_name, settings_dict_type.c.dict_type,
                      settings_dict_type.c.dict_remark, settings_dict_type.c.dict_status,
                      settings_dict_type.c.create_time, settings_dict_type.c.update_time]

    async def all(self):
        all_dict = await db.fetch_all(
            select(self.select_columns).where(settings_dict_type.c.is_delete == 0).order_by(
                settings_dict_type.c.id.desc()))
        return pydantic.parse_obj_as(List[SettingDictTypeOut], all_dict)

    async def list(self, list_in: SettingDictTypeListIn):
        where = [settings_dict_type.c.is_delete == 0]
        if list_in.dictType is not None:
            where.append(settings_dict_type.c.dict_type.like(f'%{list_in.dictType}%'))
        if list_in.dictName is not None:
            where.append(settings_dict_type.c.dict_name.like(f'%{list_in.dictName}%'))
        if list_in.dictStatus is not None:
            where.append(settings_dict_type.c.dict_status == list_in.dictStatus)
        query = select(self.select_columns).select_from(settings_dict_type).where(*where).order_by(
            settings_dict_type.c.id.desc())

        return await paginate(db, query)

    async def detail(self, _id: int):
        type_detail = await db.fetch_one(
            settings_dict_type.select().where(
                settings_dict_type.c.id == _id, settings_dict_type.c.is_delete == 0).limit(1))
        assert type_detail, '字典类型不存在！'
        return pydantic.parse_obj_as(SettingDictTypeOut, type_detail)

    async def add(self, add_in: SettingDictTypeAddIn):
        """管理员新增"""
        assert not await db.fetch_one(
            settings_dict_type.select()
            .where(settings_dict_type.c.dict_name == add_in.dict_name,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典名称已存在！'
        assert not await db.fetch_one(
            settings_dict_type.select()
            .where(settings_dict_type.c.dict_type == add_in.dict_type,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典类型已存在！'

        create_dict = dict(add_in)
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(settings_dict_type.insert().values(**create_dict))

    async def edit(self, edit_in: SettingDictTypeEditIn):
        assert await db.fetch_one(
            settings_dict_type.select()
            .where(settings_dict_type.c.id == edit_in.id,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典类型不存在！'

        assert not await db.fetch_one(
            settings_dict_type.select()
            .where(settings_dict_type.c.dict_name == edit_in.dict_name,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典名称已存在！'

        assert not await db.fetch_one(
            settings_dict_type.select()
            .where(settings_dict_type.c.dict_type == edit_in.dict_type,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典类型已存在！'

        type_edit = edit_in.dict()
        type_edit['update_time'] = int(time.time())
        return await db.execute(settings_dict_type.update()
                                .where(settings_dict_type.c.id == edit_in.id)
                                .values(**type_edit))

    async def delete(self, delete_in: SettingDictTypeDeleteIn):
        await db.execute(settings_dict_type.update()
                         .where(settings_dict_type.c.id.in_(delete_in.ids))
                         .values(is_delete=1, delete_time=int(time.time())))

    @classmethod
    async def instance(cls):
        return cls()
