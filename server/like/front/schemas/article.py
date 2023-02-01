from datetime import datetime
from enum import Enum
from typing import Union

from fastapi import Query
from pydantic import BaseModel, Field

from like.schema_base import EmptyStrToNone


class ArticleListInSortEnum(str, Enum):
    """
    文章列表搜索入参 Enum
    """
    hot = 'hot'  # 热门
    new = 'new'  # 最新
    default = ''  # 默认

class ArticleBaseOut(BaseModel):
    """
    文章 输出
    """
    id: int
    title: str
    intro: str
    image: str
    visit: int  # 浏览
    collect: bool = Field(default=False)
    createTime: datetime = Field(alias='create_time')  # 创建时间

class ArticleDetailOut(ArticleBaseOut):
    """
    文章 详情 输出
    """
    summary: str
    content: str
    author: str


class ArticleListIn(BaseModel):
    """
    文章列表 入参
    """
    cid: Union[int, None, EmptyStrToNone] = Query(default=None)  # 分类ID
    keyword: Union[str, None] = Query(default=None)  # 关键词
    sort: Union[ArticleListInSortEnum, EmptyStrToNone, None]


class ArticleDetailIn(BaseModel):
    """
    文章详情 入参
    """
    id: Union[int, None, EmptyStrToNone] = Query(default=None)


class ArticleCategoryOut(BaseModel):
    """
    文章分类 输出
    """
    id: int
    name: str = Field(default='')


class ArticleCollectOut(BaseModel):
    """
    文章收藏列表 输出
    """
    id: int
    articleId: int = Field(alias='article_id')
    title: str
    image: str
    intro: str
    visit: int  # 浏览
    createTime: datetime = Field(alias='create_time')  # 创建时间


class ArticleCollectPostIn(BaseModel):
    """
    文章加入/取消收藏 入参
    """
    article_id: int = Field(alias='articleId', default=0)
