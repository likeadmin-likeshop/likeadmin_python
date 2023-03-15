import json
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.dependencies.database import db
from like.front.schemas.article import ArticleDetailOut
from like.front.schemas.article import ArticleSearchOut
from like.front.schemas.index import IndexOut, PolicyIn, CommonProtocol
from like.front.schemas.index import SearchIn
from like.models import hot_search, article_cate_table
from like.models.article import article_table
from like.models.decorate import decorate_page
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IIndexService(ABC):
    """首页服务抽象类"""

    @abstractmethod
    async def index(self) -> IndexOut:
        pass

    @abstractmethod
    async def decorate(self, id_: int) -> dict:
        pass

    @abstractmethod
    async def config(self) -> dict:
        pass

    @abstractmethod
    async def policy(self, policy_in: PolicyIn) -> CommonProtocol:
        pass

    @abstractmethod
    async def hot_search(self) -> List[str]:
        pass

    @abstractmethod
    async def search(self, search_in: SearchIn) -> AbstractPage[ArticleSearchOut]:
        pass


class IndexService(IIndexService):
    """首页服务实现类"""

    async def index(self) -> IndexOut:
        """
        首页数据
        :return:
        """
        page_detail = await db.fetch_one(
            select(decorate_page.c.id, decorate_page.c.page_type, decorate_page.c.page_data).select_from(
                decorate_page).where(
                decorate_page.c.id == 1).limit(1))
        assert page_detail, '数据不存在！'
        pages = json.dumps(
            {"id": page_detail.id, "page_type": page_detail.page_type, "page_data": page_detail.page_data})

        article_query = select([article_table.c.id, article_table.c.cid, article_table.c.title, article_table.c.intro,
                                article_table.c.summary, article_table.c.image, article_table.c.content,
                                article_table.c.author, article_table.c.visit, article_table.c.sort,
                                article_table.c.is_show, article_table.c.create_time,
                                article_table.c.update_time]).select_from(article_table).where(
            article_table.c.is_delete == 0, article_table.c.is_show == 1).order_by(article_table.c.id.desc()).limit(20)
        articles = await db.fetch_all(article_query)
        articles = pydantic.parse_obj_as(List[ArticleDetailOut], articles)
        for article in articles:
            article.image = await UrlUtil.to_absolute_url(article.image)

        domain = UrlUtil.domain
        return pydantic.parse_obj_as(IndexOut, {"domain": domain, "pages": pages, "article": articles})

    async def decorate(self, id_: int) -> dict:
        pass

    async def config(self) -> dict:
        pass

    async def policy(self, policy_in: PolicyIn) -> CommonProtocol:
        """
        隐私政策
        :param policy_in:
        :return:
        """
        map = await ConfigUtil.get_map("protocol", policy_in.type)
        return pydantic.parse_obj_as(CommonProtocol, map)

    # async def policy(self, type_: str) -> dict:
    #     """政策"""
    #     policy_dict = await ConfigUtil.get_map('protocol', type_)
    #     if not policy_dict:
    #         return {'name': '', 'content': ''}
    #     return policy_dict

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
