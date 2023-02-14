from abc import ABC, abstractmethod
from typing import List

import pydantic

from like.admin.schemas.setting import SettingHotSearchIn, SettingHotSearchOut
from like.dependencies.database import db
from like.models import hot_search
from like.utils.config import ConfigUtil


class ISettingSearchService(ABC):
    """热门搜索服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, hot_search_in: SettingHotSearchIn):
        pass


class SettingSearchService(ISettingSearchService):
    """热门搜索服务实现类"""

    async def detail(self) -> dict:
        """热门搜索详情"""
        is_hot_search = await ConfigUtil.get_val('search', 'isHotSearch', '0')
        is_hot_search = int(is_hot_search) if is_hot_search.isdigit() else 0
        objs = await db.fetch_all(hot_search.select().order_by(hot_search.c.sort.desc()))
        return {
            'is_hot_search': is_hot_search,
            'list': pydantic.parse_obj_as(List[SettingHotSearchOut], objs),
        }

    async def save(self, hot_search_in: SettingHotSearchIn):
        """热门搜索新增"""
        await ConfigUtil.set('search', 'isHotSearch', str(hot_search_in.is_hot_search))
        await db.execute(hot_search.insert().values(hot_search_in.dict()['list']))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
