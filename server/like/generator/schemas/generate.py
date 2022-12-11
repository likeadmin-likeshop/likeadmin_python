from datetime import date, datetime
from typing import Union

from fastapi import Query
from pydantic import validator, BaseModel, Field

from like.schema_base import EmptyStrToNone


class DbTablesIn(BaseModel):
    """库表列表参数"""
    table_name: Union[str, None] = Query(alias='tableName', default=None)  # 账号
    table_comment: Union[str, None] = Query(alias='tableComment', default=None)  # 昵称


class ListTableIn(BaseModel):
    """生成列表参数"""
    table_name: Union[str, None] = Query(alias='tableName', default=None)  # 账号
    table_comment: Union[str, None] = Query(alias='tableComment', default=None)  # 昵称
    start_time: Union[date, None, EmptyStrToNone] = Query(alias='startTime')  # 开始时间
    end_time: Union[date, None, EmptyStrToNone] = Query(alias='endTime')  # 结束时间


class DetailTableIn(BaseModel):
    """生成详情参数"""
    id: int = Query()  # 主键


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


class DownloadCodeIn(BaseModel):
    """下载代码参数"""
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


class GenTableBaseOut(BaseModel):
    """生成表基本返回信息"""
    id: int  # 生成主键
    tableName: str = Field(alias='table_name')  # 表的名称
    tableComment: str = Field(alias='table_comment')  # 表的描述
    entityName: str = Field(alias='entity_name')  # 实体的名称
    authorName: str = Field(alias='author_name')  # 作者的名称
    remarks: str  # 备注信息
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True


class GenTableGenOut(BaseModel):
    """生成表生成返回信息"""
    genTpl: str = Field(alias='gen_tpl')  # 生成模板方式: [crud=单表, tree=树表]
    genType: int = Field(alias='gen_type')  # 生成代码方式: [0=zip压缩包, 1=自定义路径]
    genPath: str = Field(alias='gen_path')  # 生成代码路径: [不填默认项目路径]
    moduleName: str = Field(alias='module_name')  # 生成模块名
    functionName: str = Field(alias='function_name')  # 生成功能名
    treePrimary: str = Field(alias='tree_primary')  # 树主键字段
    treeParent: str = Field(alias='tree_parent')  # 树父级字段
    treeName: str = Field(alias='tree_name')  # 树显示字段
    subTableName: str = Field(alias='sub_table_name')  # 关联表名称
    subTableFk: str = Field(alias='sub_table_fk')  # 关联表外键

    class Config:
        orm_mode = True


class GenColumnOut(BaseModel):
    """生成列返回信息"""
    id: int  # 字段主键
    columnName: str = Field(alias='column_name')  # 字段名称
    columnComment: str = Field(alias='column_comment')  # 字段描述
    columnLength: int = Field(alias='column_length')  # 字段长度
    columnType: str = Field(alias='column_type')  # 字段类型
    pyType: str = Field(alias='java_type')  # Python类型
    pyField: str = Field(alias='java_field')  # Python字段
    isRequired: int = Field(alias='is_required')  # 是否必填
    isInsert: int = Field(alias='is_insert')  # 是否插入字段
    isEdit: int = Field(alias='is_edit')  # 是否编辑字段
    isList: int = Field(alias='is_list')  # 是否列表字段
    isQuery: int = Field(alias='is_query')  # 是否查询字段
    queryType: str = Field(alias='query_type')  # 查询方式: [等于、不等于、大于、小于、范围]
    htmlType: str = Field(alias='html_type')  # 显示类型: [文本框、文本域、下拉框、复选框、单选框、日期控件]
    dictType: str = Field(alias='dict_type')  # 字典类型
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True
