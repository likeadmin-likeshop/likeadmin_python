from datetime import datetime
from typing import List, Union

from fastapi import Query, UploadFile
from pydantic import BaseModel, Field

from like.schema_base import EmptyStrToNone


class CommonAlbumCateOut(BaseModel):
    """
    类目
    """
    id: int
    name: str = Field(default='')
    pid: int
    type: int
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间


class CommonAlbumOut(BaseModel):
    """
    文件
    """
    id: int
    cid: int
    name: str = Field(default='')
    ext: str
    size: str
    url: str = Field(alias='uri')
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间


class CommonAlbumAddIn(BaseModel):
    cid: int
    aid: int
    uid: Union[int, None] = Query(default=None)
    type: int
    name: str
    ext: str
    size: str
    url: str


class CommonAlbumDelIn(BaseModel):
    ids: List[int]


class CommonAlbumListIn(BaseModel):
    type: Union[int, None, EmptyStrToNone] = Query(default=None)
    keyword: Union[str, None] = Query(default=None)
    cid: Union[int, None, EmptyStrToNone] = Query(default=None)


class CommonAlbumCateListIn(BaseModel):
    type: Union[int, None] = Query(default=None)
    keyword: Union[str, None] = Query(default=None)


class CommonAlbumCateDelIn(BaseModel):
    id: int


class CommonAlbumRenameIn(BaseModel):
    id: int
    name: str


class CommonAlbumMoveIn(BaseModel):
    ids: List[int]
    cid: int


class CommonAlbumCateEditIn(BaseModel):
    type: Union[int, None] = Query(default=10)
    name: Union[str, None] = Query(default='')
    pid: Union[int, None] = Query(default=None)


class CommonFileUploadIn(BaseModel):
    file_in: UploadFile
    cid: int
