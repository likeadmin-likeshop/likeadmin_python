import json
from abc import ABC, abstractmethod
from typing import List

import pydantic
from sqlalchemy import select

from like.dependencies.database import db
from like.front.schemas.article import ArticleDetailOut
from like.front.schemas.index import IndexOut, PolicyIn, CommonProtocol
from like.models.article import article_table
from like.models.decorate import decorate_page
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IIndexService(ABC):

    @abstractmethod
    async def index(self) -> IndexOut:
        """
        首页数据
        :return:
        """

    @abstractmethod
    async def policy(self, policy_in: PolicyIn) -> CommonProtocol:
        """
        隐私政策
        :return:
        """


class IndexService(ABC):

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

    async def policy(self, policy_in: PolicyIn) -> CommonProtocol:
        """
        隐私政策
        :param policy_in:
        :return:
        """
        map = await ConfigUtil.get_map("protocol", policy_in.type)
        return pydantic.parse_obj_as(CommonProtocol, map)

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
