from typing import List

from fastapi import Query
from pydantic import BaseModel
from typing_extensions import Literal

from like.common.enums import PolicyTypeEnum
from like.front.schemas.article import ArticleDetailOut


class IndexOut(BaseModel):
    """
    首页数据
    """
    domain: str
    pages: str
    article: List[ArticleDetailOut]


class PolicyIn(BaseModel):
    """
    隐私政策入参
    """
    type: PolicyTypeEnum


# class PolicyIn(BaseModel):
#     """协议参数"""
#     type: Literal['service', 'privacy'] = Query()


class CommonProtocol(BaseModel):
    """
    政策通用参数
    """
    name: str  # 名称
    content: str  # 内容


class PolicyOut(BaseModel):
    """
    隐私政策
    """


class SearchIn(BaseModel):
    """搜索参数"""
    keyword: str = Query()
