import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.admin.schemas.article import ArticleCateOut, ArticleCateListIn, ArticleCateAddin, \
    ArticleCateEditIn, ArticleCateDetailIn, ArticleCateChangeIn, ArticleCateDeleteIn
from like.dependencies.database import db
from like.models.article import article_cate_table


class IArticleCateService(ABC):
    """
    文章分类服务基类
    """

    @abstractmethod
    async def all(self):
        """
        分类所有
        :return:
        """
        pass

    @abstractmethod
    async def list(self, list_in: ArticleCateListIn) -> AbstractPage[ArticleCateOut]:
        """
        分类列表
        :param list_in:
        :return:
        """
        pass

    @abstractmethod
    async def detail(self, detail_in: ArticleCateDetailIn) -> ArticleCateOut:
        """
        分类详情
        :param detail_in:
        :return:
        """
        pass

    @abstractmethod
    async def add(self, add_in: ArticleCateAddin):
        """
        分类新增
        :return:
        """
        pass

    @abstractmethod
    async def edit(self, edit_in: ArticleCateEditIn):
        """
        分类编辑
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, delete_in: ArticleCateDeleteIn):
        """
        分类删除
        :return:
        """
        pass

    @abstractmethod
    async def change(self, change_in: ArticleCateChangeIn):
        """
        分类状态修改
        :param change_in:
        :return:
        """
        pass


class ArticleCateService(IArticleCateService):
    """
    文章分类服务实现类
    """
    select_columns = [article_cate_table.c.id, article_cate_table.c.name, article_cate_table.c.sort,
                      article_cate_table.c.is_show, article_cate_table.c.create_time, article_cate_table.c.update_time]

    order_by = [article_cate_table.c.sort.desc(), article_cate_table.c.id.desc()]

    async def find_cate_by_id(self, cate_id: int):
        """
        根据id返回指定cate
        :param cate_id:
        :return:
        """
        return await db.fetch_one(
            select(self.select_columns).select_from(article_cate_table).where(
                article_cate_table.c.id == cate_id, article_cate_table.c.is_delete == 0).limit(1))

    async def all(self) -> List[ArticleCateOut]:
        """
        所有文章分类
        :return:
        """
        query = select(self.select_columns).select_from(article_cate_table).where(
            article_cate_table.c.is_delete == 0).order_by(*self.order_by)
        all_cate = await db.fetch_all(query)
        return pydantic.parse_obj_as(List[ArticleCateOut], all_cate)

    async def list(self, list_in: ArticleCateListIn) -> AbstractPage[ArticleCateOut]:
        where = [article_cate_table.c.is_delete == 0]
        if list_in.name:
            where.append(article_cate_table.c.name.like('%{0}%'.format(list_in.name)))
        if list_in.is_show is not None:
            where.append(article_cate_table.c.is_show == list_in.is_show)
        query = select(self.select_columns).select_from(article_cate_table).where(*where).order_by(*self.order_by)
        return await paginate(db, query)

    async def detail(self, detail_in: ArticleCateDetailIn) -> ArticleCateOut:
        """
        分类详情
        :param detail_in:
        :return:
        """
        cate_detail = await self.find_cate_by_id(detail_in.id)
        assert cate_detail, '分类不存在！'
        return pydantic.parse_obj_as(ArticleCateOut, cate_detail)

    async def add(self, add_in: ArticleCateAddin) -> ArticleCateOut:
        """
        分类新增
        :return:
        """
        create_cate = add_in.dict()
        create_cate['create_time'] = int(time.time())
        create_cate['update_time'] = int(time.time())
        query = article_cate_table.insert().values(**create_cate)
        return await db.execute(query)

    async def edit(self, edit_in: ArticleCateEditIn) -> ArticleCateOut:
        """
        分类编辑
        :return:
        """
        edit_cate = await self.find_cate_by_id(edit_in.id)
        assert edit_cate, '分类不存在'

        edit_dict = edit_in.dict()
        edit_dict['update_time'] = int(time.time())
        return await db.execute(article_cate_table.update()
                                .where(article_cate_table.c.id == article_cate_table.id)
                                .values(**edit_dict))

    async def delete(self, delete_in: ArticleCateDeleteIn) -> ArticleCateOut:
        """
        分类删除
        :return:
        """
        delete_cate = await self.find_cate_by_id(delete_in.id)
        assert delete_cate, '分类不存在'
        # TODO: 检查有文章使用分类

        return await db.execute(article_cate_table.update()
                                .where(article_cate_table.c.id == delete_in.id)
                                .values(is_delete=1, delete_time=int(time.time())))

    async def change(self, change_in: ArticleCateChangeIn):
        """
        分类状态
        :param change_in:
        :return:
        """
        change_cate = await self.find_cate_by_id(change_in.id)
        assert change_cate, '分类不存在'
        new_is_show = int(not bool(change_cate.is_show))
        return await db.execute(article_cate_table.update()
                                .where(article_cate_table.c.id == change_in.id)
                                .values(is_show=new_is_show, update_time=int(time.time())))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
