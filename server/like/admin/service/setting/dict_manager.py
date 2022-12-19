"""
字典管理
"""
import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi import Depends
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.admin.schemas.setting import SettingDictTypeOut, SettingDictTypeListIn, SettingDictTypeAddIn, \
    SettingDictTypeEditIn, SettingDictTypeDeleteIn, SettingDictTypeDetailIn, SettingDictDataListIn, SettingDictDataOut, \
    SettingDictDataDetailIn, SettingDictDataAddIn, SettingDictDataEditIn, SettingDictDataDeletelIn
from like.dependencies.database import db
from like.models.setting import settings_dict_type, settings_dict_data


class ISettingDictTypeService(ABC):
    """
    字典类型服务抽象类
    """

    @abstractmethod
    async def list(self, list_in: SettingDictTypeListIn) -> AbstractPage[SettingDictTypeOut]:
        pass

    @abstractmethod
    async def all(self) -> List[SettingDictTypeOut]:
        pass

    @abstractmethod
    async def detail(self, detail_in: SettingDictTypeDetailIn) -> SettingDictTypeOut:
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

    @abstractmethod
    async def get_dict_type_id_by_type(self, dict_type: str) -> int:
        pass


class ISettingDictDataService(ABC):
    """
    字典数据服务抽象类
    """

    @abstractmethod
    async def list(self, list_in: SettingDictDataListIn) -> AbstractPage[SettingDictDataOut]:
        pass

    @abstractmethod
    async def all(self, all_in: SettingDictDataListIn) -> List[SettingDictDataOut]:
        pass

    @abstractmethod
    async def detail(self, detail_in: SettingDictDataDetailIn) -> SettingDictDataOut:
        pass

    @abstractmethod
    async def add(self, add_in: SettingDictDataAddIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: SettingDictDataEditIn):
        pass

    @abstractmethod
    async def delete(self, delete_in: SettingDictDataDeletelIn):
        pass


class SettingDictTypeService(ISettingDictTypeService):
    select_columns = [settings_dict_type.c.id, settings_dict_type.c.dict_name, settings_dict_type.c.dict_type,
                      settings_dict_type.c.dict_remark, settings_dict_type.c.dict_status,
                      settings_dict_type.c.create_time, settings_dict_type.c.update_time]

    async def all(self):
        """字典类型所有"""
        all_dict = await db.fetch_all(
            select(self.select_columns).where(settings_dict_type.c.is_delete == 0).order_by(
                settings_dict_type.c.id.desc()))
        return pydantic.parse_obj_as(List[SettingDictTypeOut], all_dict)

    async def list(self, list_in: SettingDictTypeListIn):
        """字典类型列表"""
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

    async def detail(self, detail_in: SettingDictTypeDetailIn) -> SettingDictTypeOut:
        """字典类型详情"""

        type_detail = await db.fetch_one(
            select(self.select_columns).select_from(settings_dict_type).where(
                settings_dict_type.c.id == detail_in.id, settings_dict_type.c.is_delete == 0).limit(1))
        assert type_detail, '字典类型不存在！'
        return pydantic.parse_obj_as(SettingDictTypeOut, type_detail)

    async def add(self, add_in: SettingDictTypeAddIn):
        """字典类型新增"""
        assert not await db.fetch_one(
            select([settings_dict_type.c.id]).select_from(settings_dict_type)
            .where(settings_dict_type.c.dict_name == add_in.dict_name,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典名称已存在！'
        assert not await db.fetch_one(
            select([settings_dict_type.c.id]).select_from(settings_dict_type)
            .where(settings_dict_type.c.dict_type == add_in.dict_type,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典类型已存在！'

        create_dict = dict(add_in)
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(settings_dict_type.insert().values(**create_dict))

    async def edit(self, edit_in: SettingDictTypeEditIn):
        assert await db.fetch_one(
            select([settings_dict_type.c.id]).select_from(settings_dict_type)
            .where(settings_dict_type.c.id == edit_in.id,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典类型不存在！'

        assert not await db.fetch_one(
            select([settings_dict_type.c.id]).select_from(settings_dict_type)
            .where(settings_dict_type.c.dict_name == edit_in.dict_name,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典名称已存在！'

        assert not await db.fetch_one(
            select([settings_dict_type.c.id]).select_from(settings_dict_type)
            .where(settings_dict_type.c.dict_type == edit_in.dict_type,
                   settings_dict_type.c.is_delete == 0).limit(1)), '字典类型已存在！'

        type_edit = edit_in.dict()
        type_edit['update_time'] = int(time.time())
        return await db.execute(settings_dict_type.update()
                                .where(settings_dict_type.c.id == edit_in.id)
                                .values(**type_edit))

    async def delete(self, delete_in: SettingDictTypeDeleteIn):
        """
        删除字典类型
        :param delete_in:
        :return:
        """
        await db.execute(settings_dict_type.update()
                         .where(settings_dict_type.c.id.in_(delete_in.ids))
                         .values(is_delete=1, delete_time=int(time.time())))

    async def get_dict_type_id_by_type(self, dict_type: str) -> int:
        """
        根据字典类型， 返回字典类型的id
        :param dict_type:
        :return:
        """
        result = await db.fetch_one(
            select([settings_dict_type.c.id]).select_from(settings_dict_type).where(
                settings_dict_type.c.dict_type == dict_type, settings_dict_type.c.is_delete == 0).limit(1))
        assert result, "该字典类型不存在"
        return result.id

    @classmethod
    async def instance(cls):
        return cls()


class SettingDictDataService(ISettingDictDataService):
    """
    字典数据服务抽象类
    """
    select_columns = [settings_dict_data.c.id, settings_dict_data.c.type_id, settings_dict_data.c.name,
                      settings_dict_data.c.value, settings_dict_data.c.remark,
                      settings_dict_data.c.sort, settings_dict_data.c.status, settings_dict_data.c.create_time,
                      settings_dict_data.c.update_time]

    async def list(self, list_in: SettingDictDataListIn) -> AbstractPage[SettingDictDataOut]:
        """
        字典数据-列表
        :param list_in:
        :return:
        """
        dict_type_id = await self.dict_type_service.get_dict_type_id_by_type(list_in.dictType)
        query = self.get_dict_data_list_query(list_in, dict_type_id)
        return await paginate(db, query)

    async def all(self, all_in: SettingDictDataListIn) -> List[SettingDictDataOut]:
        """
        字典数据-所有
        :param all_in:
        :return:
        """
        dict_type_id = await self.dict_type_service.get_dict_type_id_by_type(all_in.dictType)
        query = self.get_dict_data_list_query(all_in, dict_type_id)
        all_dict = await db.fetch_all(query)
        return pydantic.parse_obj_as(List[SettingDictDataOut], all_dict)

    def get_dict_data_list_query(self, params: SettingDictDataListIn, dict_type_id: int):
        """
        all、list的搜索条件一致
        :param params:
        :return:
        """
        where = [settings_dict_data.c.is_delete == 0, settings_dict_data.c.type_id == dict_type_id]
        if params.name is not None:
            where.append(settings_dict_data.c.name.like(f'%{params.name}%'))
        if params.value is not None:
            where.append(settings_dict_data.c.value.like(f'%{params.value}%'))
        if params.status is not None:
            where.append(settings_dict_data.c.status == params.status)
        return select(self.select_columns).select_from(settings_dict_data).where(*where).order_by(
            settings_dict_data.c.id.desc())

    async def detail(self, detail_in: SettingDictDataDetailIn) -> SettingDictDataOut:
        """
        字典数据-详情
        :param detail_in:
        :return:
        """
        data_detail = await db.fetch_one(
            select(self.select_columns).select_from(settings_dict_data).where(
                settings_dict_data.c.id == detail_in.id, settings_dict_data.c.is_delete == 0).limit(1))
        assert data_detail, '字典数据不存在！'
        return pydantic.parse_obj_as(SettingDictDataOut, data_detail)

    async def add(self, add_in: SettingDictDataAddIn):
        """
        字典数据-新增
        :param add_in:
        :return:
        """
        assert not await db.fetch_one(
            select([settings_dict_data.c.id]).select_from(settings_dict_data)
            .where(settings_dict_data.c.name == add_in.name,
                   settings_dict_data.c.is_delete == 0).limit(1)), '字典数据已存在！'
        create_dict = dict(add_in)
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(settings_dict_data.insert().values(**create_dict))

    async def edit(self, edit_in: SettingDictDataEditIn):
        assert await db.fetch_one(
            select([settings_dict_data.c.id]).select_from(settings_dict_data)
            .where(settings_dict_data.c.id == edit_in.id,
                   settings_dict_data.c.is_delete == 0).limit(1)), '字典数据不存在！'
        assert not await db.fetch_one(
            select([settings_dict_data.c.id]).select_from(settings_dict_data)
            .where(settings_dict_data.c.name == edit_in.name,
                   settings_dict_data.c.is_delete == 0).limit(1)), '字典数据已存在！'
        type_edit = edit_in.dict()
        type_edit['update_time'] = int(time.time())
        return await db.execute(settings_dict_data.update()
                                .where(settings_dict_data.c.id == edit_in.id)
                                .values(**type_edit))

    async def delete(self, delete_in: SettingDictDataDeletelIn):
        """
        删除字典数据
        :param delete_in:
        :return:
        """
        await db.execute(settings_dict_data.update()
                         .where(settings_dict_data.c.id.in_(delete_in.ids))
                         .values(is_delete=1, delete_time=int(time.time())))

    def __init__(self, dict_type_service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
        self.dict_type_service: ISettingDictTypeService = dict_type_service

    @classmethod
    async def instance(cls, dict_type_service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
        return cls(dict_type_service)
