from datetime import datetime
from typing import Union

from fastapi import Query
from pydantic import validator, BaseModel, Field


class DbTablesIn(BaseModel):
    """库表列表参数"""
    table_name: Union[str, None] = Query(alias='tableName', default=None)  # 账号
    table_comment: Union[str, None] = Query(alias='tableComment', default=None)  # 昵称


class ImportTableIn(BaseModel):
    """表导入参数"""
    tables: str = Query()  # 导入的表, 用","分隔


class EditTableIn(BaseModel):
    """表编辑参数"""
    pass


class PreviewCodeIn(BaseModel):
    """预览代码参数"""
    id: int = Query()  # 主键


class GenCodeIn(BaseModel):
    """生成代码参数"""
    tables: str = Query()  # 导入的表, 用","分隔


class DbTableOut(BaseModel):
    """数据表返回信息"""
    tableName: str = Field(alias='table_name')  # 表的名称
    tableComment: str = Field(alias='table_comment')  # 表的描述
    # authorName: Union[str, None] = Field(alias='author_name')  # 作者名称
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: Union[datetime, None] = Field(alias='update_time')  # 更新时间

    @validator('updateTime')
    def set_update_time(cls, update_time):
        return update_time or ''

    class Config:
        orm_mode = True


class GenTableOut(BaseModel):
    """生成表返回信息"""
    id: int  # 生成主键
    genType: int = Field(alias='gen_type')  # 生成类型: [0=zip压缩包, 1=自定义路径]
    tableName: str = Field(alias='table_name')  # 表的名称
    tableComment: str = Field(alias='table_comment')  # 表的描述
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True
