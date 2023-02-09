from datetime import date, datetime
from typing import Union

from fastapi import Query
from pydantic import BaseModel, Field

from like.schema_base import EmptyStrToNone


class ArticleCateOut(BaseModel):
    """
    文章分类输出
    """
    id: int
    name: str = Field(default='')
    sort: int
    isShow: int = Field(alias='is_show')
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间


class ArticleCateListIn(BaseModel):
    """
    文章分类列表入参
    """
    name: Union[str, None] = Query(default=None)
    is_show: Union[int, None] = Query(default=1, alias='isShow')


class ArticleCateDetailIn(BaseModel):
    """
    文章分类详情入参
    """
    id: int = Query(gt=0)  # 主键


class ArticleCateAddIn(BaseModel):
    """
    文章分类新增入参
    """
    name = str
    sort: int = Field(ge=0)  # 排序
    is_show: int = Field(alias='isShow', ge=0, le=1)  # 是否显示: [0=否, 1=是]


class ArticleCateEditIn(ArticleCateAddIn):
    """
    文章分类修改入参
    """
    id: int = Query(gt=0)  # 主键


class ArticleCateDeleteIn(BaseModel):
    """
    文章分类删除入参
    """
    id: int = Query(gt=0)  # 主键


class ArticleCateChangeIn(BaseModel):
    """
    文章分类状态修改入参
    """
    id: int = Query(gt=0)  # 主键


class ArticleListIn(BaseModel):
    """
    文章列表
    """
    title: str = Query(default='')
    cid: Union[int, None, EmptyStrToNone] = Query(default=None)
    is_show: Union[int, None, EmptyStrToNone] = Field(alias='isShow', ge=0, le=1, default=1)  # 是否显示: [0=否, 1=是]
    start_time: Union[date, None, EmptyStrToNone] = Query(alias='startTime')  # 开始时间
    end_time: Union[date, None, EmptyStrToNone] = Query(alias='endTime')  # 结束时间


class ArticleDetailIn(BaseModel):
    """
    文章详情
    """
    id: Union[int, None, EmptyStrToNone] = Query(default=None)


class ArticleAddIn(BaseModel):
    """
    新增文章
    """
    title: str
    cid: int
    intro: str
    summary: str
    author: str
    content: str
    sort: str
    is_show: int = Field(alias='isShow', ge=0, le=1)  # 是否显示: [0=否, 1=是]


class ArticleDeleteIn(BaseModel):
    """
    文章删除
    """
    id: int


class ArticleChangeIn(BaseModel):
    """
    文章修改状态
    """
    id: int


class ArticleEditIn(ArticleAddIn):
    """
    编辑文章
    """
    id: int


class ArticleListOut(BaseModel):
    """
    文章 列表输出
    """
    id: int
    category: str = Field(alias='name')
    title: str
    intro: str
    image: str
    author: str
    sort: int
    visit: int  # 浏览
    isShow: int = Field(alias='is_show', ge=0, le=1)  # 是否显示: [0=否, 1=是]
    createTime: datetime = Field(alias='create_time')
    updateTime: datetime = Field(alias='update_time')  # 更新时间


class ArticleDetailOut(BaseModel):
    """
    文章 详情输出
    """
    id: int
    cid: int
    title: str
    intro: str
    image: str
    summary: str
    content: str
    author: str
    sort: int
    visit: int  # 浏览
    isShow: int = Field(alias="is_show", ge=0, le=1)  # 是否显示: [0=否, 1=是]
    createTime: datetime = Field(alias='create_time')
    updateTime: datetime = Field(alias='update_time')  # 更新时间
