from fastapi import Query
from pydantic import BaseModel
from typing_extensions import Literal


class PolicyIn(BaseModel):
    """协议参数"""
    type: Literal['service', 'privacy'] = Query()


class SearchIn(BaseModel):
    """搜索参数"""
    keyword: str = Query()
