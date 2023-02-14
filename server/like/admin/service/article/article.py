import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.admin.schemas.article import ArticleEditIn, ArticleChangeIn, ArticleDeleteIn, ArticleListIn, ArticleDetailIn, \
    ArticleDetailOut, \
    ArticleListOut, ArticleAddIn
from like.dependencies.database import db
from like.models.article import article_table, article_cate_table
from like.utils.urls import UrlUtil


class IArticleService(ABC):
    """
    文章服务基类(admin)
    """

    @abstractmethod
    async def list(self, list_in: ArticleListIn) -> List[ArticleListOut]:
        """
        文章新增
        :return:
        """
        pass

    async def detail(self, detail_in: ArticleDetailIn) -> ArticleDetailOut:
        """
        文章详情
        :return:
        """
        pass

    @abstractmethod
    async def add(self, add_in: ArticleAddIn):
        """
        文章新增
        :return:
        """
        pass

    @abstractmethod
    async def edit(self, edit_in: ArticleEditIn):
        """
        文章编辑
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, delete_in: ArticleDeleteIn):
        """
        文章删除
        :return:
        """
        pass

    @abstractmethod
    async def change(self, change_in: ArticleChangeIn):
        """
        文章状态修改
        :param change_in:
        :return:
        """
        pass


class ArticleService(IArticleService):
    """
    文章分类服务实现类
    """
    select_columns = [article_table.c.id, article_table.c.cid, article_table.c.title, article_table.c.image,
                      article_table.c.intro, article_table.c.summary, article_table.c.content, article_table.c.author,
                      article_table.c.sort, article_table.c.visit, article_table.c.is_show, article_table.c.create_time,
                      article_table.c.update_time]

    order_by = [article_cate_table.c.sort.desc(), article_cate_table.c.id.desc()]

    async def list_limit(self, limit) -> List[ArticleDetailOut]:
        where = [article_table.c.is_delete == 0, article_table.c.is_show == 1]
        article_list = select(self.select_columns).where(*where).select_from(
            article_table.outerjoin(article_cate_table, article_table.c.cid == article_cate_table.c.id)).order_by(
            article_table.c.id.desc()).limit(limit)
        articles = await db.fetch_all(article_list)
        return pydantic.parse_obj_as(List[ArticleDetailOut], articles)

    async def list(self, list_in: ArticleListIn) -> List[ArticleListOut]:
        """
        返回用户收藏的文章ID
        :param list_in:
        :return:
        """
        colums = self.select_columns + [article_cate_table.c.name]
        where = [article_table.c.is_delete == 0]
        if list_in.title:
            where.append(article_table.c.title.like("%{0}%".format(list_in.title)))
        if list_in.cid:
            where.append(article_table.c.cid == list_in.cid)
        if list_in.is_show is not None:
            where.append(article_table.c.is_show == list_in.is_show)
        if list_in.start_time:
            where.append(article_table.c.create_time >= int(time.mktime(list_in.start_time.timetuple())))
        if list_in.end_time:
            where.append(article_table.c.create_time <= int(time.mktime(list_in.end_time.timetuple())))

        article_list = select(colums).where(*where).select_from(
            article_table.outerjoin(article_cate_table, article_table.c.cid == article_cate_table.c.id)).order_by(
            article_table.c.sort.desc(), article_table.c.id.desc()
        )
        article_list_pages = await paginate(db, article_list)
        for row in article_list_pages.lists:
            row.image = await UrlUtil.to_absolute_url(row.image)
        return article_list_pages

    async def detail(self, detail_in: ArticleDetailIn) -> ArticleDetailOut:
        """
        文章详情
        :return:
        """
        article_detail = await db.fetch_one(
            select(self.select_columns).select_from(article_table).where(
                article_table.c.id == detail_in.id, article_table.c.is_delete == 0).limit(1))
        assert article_detail, '文章不存在！'
        result = pydantic.parse_obj_as(ArticleDetailOut, article_detail)
        result.image = await UrlUtil.to_absolute_url(article_detail.image)
        return result

    async def add(self, add_in: ArticleAddIn):
        """
        添加文章
        :param add_in:
        :return:
        """
        add_article_dict = add_in.dict()
        add_article_dict['create_time'] = int(time.time())
        add_article_dict['update_time'] = int(time.time())
        query = article_table.insert().values(**add_article_dict)
        return await db.execute(query)

    async def edit(self, edit_in: ArticleEditIn):
        """
        文章编辑
        :return:
        """

        edit_article = await db.fetch_one(
            select(self.select_columns).select_from(article_table).where(
                article_table.c.id == edit_in.id, article_table.c.is_delete == 0).limit(1))
        assert edit_article, '文章不存在！'

        edit_article_dict = edit_in.dict()
        edit_article_dict['update_time'] = int(time.time())

        return await db.execute(article_table.update()
                                .where(article_table.c.id == edit_in.id)
                                .values(**edit_article_dict))

    async def delete(self, delete_in: ArticleDeleteIn):
        """
        文章删除
        :return:
        """
        article_delete = await db.fetch_one(
            select(self.select_columns).select_from(article_table).where(
                article_table.c.id == delete_in.id, article_table.c.is_delete == 0).limit(1))
        assert article_delete, '文章不存在！'

        return await db.execute(article_table.update()
                                .where(article_table.c.id == delete_in.id)
                                .values(delete_time=int(time.time()), is_delete=True))

    async def change(self, change_in: ArticleChangeIn):
        """
        文章状态修改
        :param change_in:
        :return:
        """
        article_change = await db.fetch_one(
            select(self.select_columns).select_from(article_table).where(
                article_table.c.id == change_in.id, article_table.c.is_delete == 0).limit(1))
        assert article_change, '文章不存在！'

        new_show_value = not bool(article_change.is_show)

        return await db.execute(article_table.update()
                                .where(article_table.c.id == change_in.id)
                                .values(update_time=int(time.time()), is_show=new_show_value))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
