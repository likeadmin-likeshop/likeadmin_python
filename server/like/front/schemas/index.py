from typing import List

from pydantic import BaseModel

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
