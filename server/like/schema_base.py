from typing import Union, TypeVar, Generic, Sequence

from fastapi import Query
from fastapi_pagination.bases import AbstractParams, AbstractPage, RawParams
from pydantic import BaseModel
from pydantic.validators import str_validator

T = TypeVar("T")
C = TypeVar("C")


class PageParams(BaseModel, AbstractParams):
    pageNo: int = Query(1, ge=1, description='Page Number')
    pageSize: int = Query(20, gt=0, le=60, description='Page Size')

    def to_raw_params(self) -> RawParams:
        offset = (self.pageNo - 1) * self.pageSize
        return RawParams(limit=self.pageSize, offset=offset)


class PageInationResult(AbstractPage[T], Generic[T]):
    """
    分页结果封装
        items: 返回集列表
        total: 结果总数
    """
    count: int
    pageNo: int
    pageSize: int
    lists: Sequence[T]

    __params_type__ = PageParams

    @classmethod
    def create(cls, items: Sequence[T], total: int, params: PageParams):
        return cls(lists=items, count=total, pageNo=params.pageNo, pageSize=params.pageSize)


def empty_to_none(v: str) -> Union[str, None]:
    """替换空字符为None"""
    if v == '':
        return None
    return v


class EmptyStrToNone(str):
    """空字符串替换类型
        针对非str类型，可传空字符串类型校验
    """

    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none
