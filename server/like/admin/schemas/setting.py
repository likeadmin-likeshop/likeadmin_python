from datetime import datetime
from typing import List, Union

from pydantic import BaseModel, Field

from like.admin.schemas.system import EmptyStrToNone


class SettingWebsiteIn(BaseModel):
    """
    保存网站信息参数
    """
    name: str = Field(default='')  # 网站名称
    logo: str = Field(default='')  # 网站图标
    favicon: str = Field(default='')  # 网站LOGO
    backdrop: str = Field(default='')  # 登录页广告图
    shop_name: str = Field(default='', alias='shopName')  # 商城名称
    shop_logo: str = Field(default='', alias='shopLogo')  # 商城Logo


class SettingCopyrightItem(BaseModel):
    """
    备案通用参数
    """
    name: str  # 名称
    link: str  # 链接


class SettingCopyrightIn(BaseModel):
    """
    保存备案信息参数
    """
    __root__: List[SettingCopyrightItem]


class CommonProtocol(BaseModel):
    """
    政策通用参数
    """
    name: str  # 名称
    content: str  # 内容


class SettingProtocolIn(BaseModel):
    """
    保存政策信息参数
    """
    service: CommonProtocol  # 服务协议
    privacy: CommonProtocol  # 隐私协议


class SettingStorageDetailIn(BaseModel):
    """存储设置详情入参"""
    alias: str


class SettingStorageEditIn(BaseModel):
    """存储设置配置入参"""
    alias: str
    status: int
    bucket: Union[str, None]
    secretKey: Union[str, None]
    accessKey: Union[str, None]
    domain: Union[str, None]
    region: Union[str, None]


class SettingStorageChangeIn(BaseModel):
    """切换存储入参"""
    alias: str
    status: int


class SettingStorageOut(BaseModel):
    """存储设置列表返回"""
    alias: str
    status: int
    describe: str = ""


class SettingStorageDetailOut(SettingStorageOut):
    """存储设置详情返回"""
    bucket: str = ""
    secretKey: str = ""
    accessKey: str = ""
    domain: str = ""


class SettingDictTypeListIn(BaseModel):
    """
    字典类型-列表 入参
    """
    dictName: Union[str, None, EmptyStrToNone]
    dictType: Union[str, None, EmptyStrToNone]
    dictStatus: Union[int, None, EmptyStrToNone]


class SettingDictTypeAddIn(BaseModel):
    """
    字典类型-新增 入参
    """
    dict_name: str = Field(alias='dictName')
    dict_type: str = Field(alias='dictType')
    dict_remark: Union[str, None] = Field(alias='dictRemark')
    dict_status: int = Field(alias='dictStatus')


class SettingDictTypeEditIn(SettingDictTypeAddIn):
    """
    字典类型-编辑 入参
    """
    id: int


class SettingDictTypeDetailIn(BaseModel):
    """
    字典类型-删除 入参
    """
    id: int


class SettingDictTypeDeleteIn(BaseModel):
    """
    字典类型-删除 入参
    """
    ids: List[int]


class SettingDictTypeOut(BaseModel):
    """
    字典类型 返回
    """
    id: int
    dictName: str = Field(alias='dict_name')
    dictType: str = Field(alias='dict_type')
    dictRemark: str = Field(alias='dict_remark')
    dictStatus: int = Field(alias='dict_status')
    createTime: datetime = Field(alias='create_time')
    updateTime: datetime = Field(alias='update_time')


class SettingDictDataListIn(BaseModel):
    """
    字典数据-列表 入参
    """
    dictType: str
    name: Union[str, None, EmptyStrToNone]
    value: Union[str, None, EmptyStrToNone]
    status: Union[int, None, EmptyStrToNone]


class SettingDictDataDetailIn(BaseModel):
    """
    字典数据-详情 入参
    """
    id: int


class SettingDictDataDeletelIn(BaseModel):
    """
    字典数据-删除 入参
    """
    ids: List[int]


class SettingDictDataAddIn(BaseModel):
    """
    字典数据-新增 入参
    """
    type_id: int = Field(alias='typeId')
    name: str
    value: str
    remark: str
    sort: int
    status: int


class SettingDictDataEditIn(SettingDictDataAddIn):
    """
    字典数据-编辑 入参
    """
    id: int


class SettingDictDataOut(BaseModel):
    """
    字典类型 返回
    """
    id: int
    typeId: int = Field(alias='type_id')
    name: str
    value: str
    remark: str
    sort: int
    status: int
    createTime: datetime = Field(alias='create_time')
    updateTime: datetime = Field(alias='update_time')
