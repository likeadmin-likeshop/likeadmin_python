from datetime import datetime
from typing import List, Union

from fastapi.params import Query
from pydantic import BaseModel, Field


class DecoratePageSaveIn(BaseModel):
    id: int = Query(gt=0)
    page_type: int = Query(alias='pageType')
    page_data: str = Query(alias='pageData')


class DecoratePageDetailOut(BaseModel):
    id: int
    page_type: int
    page_data: str


class DecorateDataArticleIn(BaseModel):
    limit: int = Query(default=10)


class DecorateTabbarStyle(BaseModel):
    defaultColor: str
    selectedColor: str


class DecorateTabbarListIn(BaseModel):
    name: Union[str, None] = Field(default=None)
    selected: Union[str, None] = Field(default=None)
    unselected: Union[str, None] = Field(default=None)
    link: Union[str, None] = Field(default=None)


class DecorateTabbarList(BaseModel):
    id: int
    name: str
    selected: str
    unselected: str
    link: str
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间


class DecorateTabbarOut(BaseModel):
    style: DecorateTabbarStyle
    list: List[DecorateTabbarList]


class DecorateTabbarSaveIn(BaseModel):
    style: DecorateTabbarStyle
    list: List[DecorateTabbarListIn]
