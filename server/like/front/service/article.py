import time
from abc import ABC, abstractmethod
from typing import List, Optional

import pydantic
from fastapi import Request
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.dependencies.database import db
from like.front.schemas.article import ArticleDetailOut, ArticleListIn, ArticleDetailIn, ArticleCategoryOut, \
    ArticleBaseOut, ArticleCollectPostIn, ArticleCollectOut
from like.models.article import article_table, article_collect_table, article_cate_table
from like.utils.urls import UrlUtil


class IArticleService(ABC):
    """
    文章服务基类(admin)
    """

    @abstractmethod
    async def list(self, list_in: ArticleListIn) -> AbstractPage[ArticleBaseOut]:
        """
        文章列表
        :param list_in:
        :return:
        """
        pass

    @abstractmethod
    async def detail(self, detail_in: ArticleDetailIn) -> ArticleDetailOut:
        """
        文章详情
        :param detail_in:
        :return:
        """
        pass

    @abstractmethod
    async def category(self) -> List[ArticleCategoryOut]:
        """
        文章分类
        :return:
        """
        pass

    @abstractmethod
    async def collect(self) -> List[ArticleCollectOut]:
        """
        收藏列表
        :return:
        """
        pass

    @abstractmethod
    async def add_collect(self, post_in: ArticleCollectPostIn):
        """
        添加收藏
        :param post_in
        :return:
        """
        pass

    @abstractmethod
    async def cancel_collect(self, post_in: ArticleCollectPostIn):
        """
        取消收藏
        :param post_in:
        :return:
        """
        pass


class ArticleService(IArticleService):
    """
    文章服务实现类
    """
    select_columns = [article_table.c.id, article_table.c.cid, article_table.c.title, article_table.c.intro,
                      article_table.c.summary, article_table.c.image, article_table.c.content,
                      article_table.c.author, article_table.c.visit, article_table.c.sort,
                      article_table.c.is_show, article_table.c.create_time,
                      article_table.c.update_time]

    article_order_by = [article_table.c.sort.desc(), article_table.c.id.desc()]
    cate_order_by = [article_cate_table.c.sort.desc(), article_cate_table.c.id.desc()]
    collect_order_by = [article_collect_table.c.id.desc()]

    def __init__(self, request: Request):
        self.request: Request = request
        self.user_id = getattr(request.state, 'user_id', None)

    async def get_user_collect_article_ids(self, user_id: int, article_ids: Optional[List[int]]) -> List[int]:
        """
        返回用户收藏的文章ID
        :param user_id:
        :param article_ids:
        :return:
        """
        where = [article_collect_table.c.user_id == user_id, article_collect_table.c.is_delete == False]
        if article_ids:
            where.append(article_collect_table.c.article_id.in_(article_ids))
        query = select([article_collect_table.c.article_id]).select_from(
            article_collect_table).where(*where)
        collects = await db.fetch_all(query)
        return [c.article_id for c in collects]

    async def update_article_visit(self, article_id: int):
        """
        文章访问数 +1
        :param article_id:
        :return:
        """
        return await db.execute(article_table.update()
                                .where(article_table.c.id == article_id)
                                .values(visit=article_table.c.visit + 1))

    async def category(self) -> List[ArticleCategoryOut]:
        """
        文章分类列表
        :return:
        """
        where = [article_cate_table.c.is_delete == 0, article_cate_table.c.is_show == 1]
        query = select([article_cate_table.c.id, article_cate_table.c.name]).select_from(
            article_cate_table).where(*where).order_by(*self.cate_order_by)
        all_cate = await db.fetch_all(query)
        return pydantic.parse_obj_as(List[ArticleCategoryOut], all_cate)

    async def list(self, list_in: ArticleListIn) -> AbstractPage[ArticleBaseOut]:
        """
        文章列表
        :param list_in:
        :return:
        """
        where = [article_table.c.is_delete == 0, article_table.c.is_show == 1]
        if list_in.cid:
            where.append(article_table.c.cid == list_in.cid)
        if list_in.keyword is not None:
            where.append(article_table.c.title.like('%{0}%'.format(list_in.keyword)))
        order_by = self.article_order_by

        if list_in.sort:
            if list_in.sort == 'hot':
                order_by = [article_table.c.visit.desc(), article_table.c.id.desc()]
            elif list_in.sort == 'new':
                order_by = [article_table.c.id.desc()]

        query = select(self.select_columns).select_from(article_table).where(*where).order_by(*order_by)
        page_result = await paginate(db, query)
        # 补充收藏信息/image转换为绝对地址
        article_ids = [row.id for row in page_result.lists]
        article_collects = []
        if self.user_id:
            article_collects = await self.get_user_collect_article_ids(user_id=self.user_id, article_ids=article_ids)
        for row in page_result.lists:
            row.image = await UrlUtil.to_absolute_url(row.image)
            if article_collects:
                row.collect = bool(row.id in article_collects)
        return page_result

    async def detail(self, detail_in: ArticleDetailIn) -> ArticleDetailOut:
        """
        文章详情
        :param detail_in:
        :return:
        """
        article_detail = await db.fetch_one(
            select(self.select_columns).select_from(article_table).where(
                article_table.c.id == detail_in.id, article_table.c.is_delete == 0).limit(1))
        assert article_detail, '数据不存在！'

        result = pydantic.parse_obj_as(ArticleDetailOut, article_detail)
        result.image = await UrlUtil.to_absolute_url(result.image)
        if self.user_id:
            article_collects = await self.get_user_collect_article_ids(user_id=self.user_id,
                                                                       article_ids=[article_detail.id])
            result.collect = bool(article_detail.id in article_collects)
        await self.update_article_visit(article_detail.id)
        return result

    async def collect(self) -> AbstractPage[ArticleCollectOut]:
        """
        收藏列表
        :return:
        """
        if not self.user_id:
            return []
        colums = [article_collect_table.c.article_id, article_collect_table.c.id,
                  article_table.c.title, article_table.c.intro,
                  article_table.c.summary, article_table.c.image, article_table.c.visit,
                  article_table.c.create_time,
                  ]
        collect_query = select(colums).where(article_collect_table.c.user_id == self.user_id,
                                             article_collect_table.c.is_delete == False,
                                             article_table.c.is_delete == False) \
            .select_from(
            article_collect_table.outerjoin(article_table,
                                            article_collect_table.c.article_id == article_table.c.id)) \
            .order_by(article_collect_table.c.id.desc())

        collect_pages = await paginate(db, collect_query)
        for row in collect_pages.lists:
            row.image = await UrlUtil.to_absolute_url(row.image)
        return collect_pages

    async def add_collect(self, post_in: ArticleCollectPostIn):
        """
        添加收藏
        :param post_in
        :return:
        """
        article_collect = await db.fetch_one(
            select([article_collect_table.c.id, article_collect_table.c.article_id,
                    article_collect_table.c.user_id]).select_from(article_collect_table).where(
                article_collect_table.c.user_id == self.user_id,
                article_collect_table.c.article_id == post_in.article_id).limit(1))
        if article_collect:
            # 已有收藏记录
            return await db.execute(article_collect_table.update()
                                    .where(article_collect_table.c.id == article_collect.id)
                                    .values(is_delete=False, update_time=int(time.time())))
        else:
            # 新增收藏记录
            collect_create = {
                'user_id': self.user_id,
                'article_id': post_in.article_id,
                'create_time': int(time.time()),
                'update_time': int(time.time())
            }

            return await db.execute(article_collect_table.insert().values(**collect_create))

    async def cancel_collect(self, post_in: ArticleCollectPostIn):
        """
        取消收藏
        :param post_in:
        :return:
        """
        article_collect = await db.fetch_one(
            select([article_collect_table.c.id]).select_from(article_collect_table).where(
                article_collect_table.c.user_id == self.user_id,
                article_collect_table.c.is_delete == False,
                article_collect_table.c.article_id == post_in.article_id).limit(1))
        assert article_collect, '收藏不存在!'
        return await db.execute(article_collect_table.update()
                                .where(article_collect_table.c.id == article_collect.id)
                                .values(is_delete=True, update_time=int(time.time())))

    @classmethod
    async def instance(cls, request: Request):
        """实例化"""
        return cls(request=request)
