from abc import ABC, abstractmethod
from typing import List

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.dependencies.database import db
from like.front.schemas.article import ArticleSearchOut
from like.front.schemas.index import SearchIn
from like.models import hot_search, article_table, article_cate_table
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IIndexService(ABC):
    """首页服务抽象类"""

    @abstractmethod
    async def index(self) -> dict:
        pass

    @abstractmethod
    async def decorate(self, id_: int) -> dict:
        pass

    @abstractmethod
    async def config(self) -> dict:
        pass

    @abstractmethod
    async def policy(self, type_: str) -> dict:
        pass

    @abstractmethod
    async def hot_search(self) -> List[str]:
        pass

    @abstractmethod
    async def search(self, search_in: SearchIn) -> AbstractPage[ArticleSearchOut]:
        pass


class IndexService(IIndexService):
    """首页服务实现类"""

    async def index(self) -> dict:
        pass

    async def decorate(self, id_: int) -> dict:
        pass

    async def config(self) -> dict:
        pass

    async def policy(self, type_: str) -> dict:
        """政策"""
        policy_dict = await ConfigUtil.get_map('protocol', type_)
        if not policy_dict:
            return {'name': '', 'content': ''}
        return policy_dict

    async def hot_search(self) -> List[str]:
        """热搜"""
        is_hot_search = await ConfigUtil.get_val('search', 'isHotSearch', '0')
        names = []
        if is_hot_search == '1':
            objs = await db.fetch_all(hot_search.select().order_by(hot_search.c.sort.desc(), hot_search.c.id.desc()))
            for obj in objs:
                names.append(obj.name)
        return names

    async def search(self, search_in: SearchIn) -> AbstractPage[ArticleSearchOut]:
        """搜索"""
        columns = [article_table, article_cate_table.c.name.label('category')]
        query = select(columns).where(
            article_table.c.is_delete == 0, article_table.c.title.like(f'%{search_in.keyword}%')) \
            .select_from(
            article_table.outerjoin(
                article_cate_table, article_table.c.cid == article_cate_table.c.id)) \
            .order_by(article_table.c.sort.desc(), article_table.c.id.desc())
        pager = await paginate(db, query)
        for row in pager.lists:
            row.collect = False
            row.image = await UrlUtil.to_absolute_url(row.image)
        return pager

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
