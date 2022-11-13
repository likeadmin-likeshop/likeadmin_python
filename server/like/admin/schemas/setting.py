from typing import List, Union

from pydantic import BaseModel, Field


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


class SettingsStorageDetailIn(BaseModel):
    """存储设置详情入参"""
    alias: str


class SettingsStorageEditIn(BaseModel):
    """存储设置配置入参"""
    alias: str
    status: int
    bucket: Union[str, None]
    secretKey: Union[str, None]
    accessKey: Union[str, None]
    domain: Union[str, None]
    region: Union[str, None]


class SettingsStorageChangeIn(BaseModel):
    """切换存储入参"""
    alias: str
    status: int


class SettingsStorageOut(BaseModel):
    """存储设置列表返回"""
    alias: str
    status: int
    describe: str = ""


class SettingsStorageDetailOut(SettingsStorageOut):
    """存储设置详情返回"""
    bucket: str = ""
    secretKey: str = ""
    accessKey: str = ""
    domain: str = ""
