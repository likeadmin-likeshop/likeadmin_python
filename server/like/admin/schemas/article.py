from datetime import datetime
from typing import Union

from fastapi import Query
from pydantic import BaseModel, Field


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


class ArticleCateAddin(BaseModel):
    """
    文章分类新增入参
    """
    name = str
    sort: int = Field(ge=0)  # 排序
    is_show: int = Field(alias='isShow', ge=0, le=1)  # 是否显示: [0=否, 1=是]


class ArticleCateEditIn(ArticleCateAddin):
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
