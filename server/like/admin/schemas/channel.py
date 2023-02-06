from typing import List

from pydantic import BaseModel, Field
from typing_extensions import Literal


class ChannelOaIn(BaseModel):
    """
    公众号渠道参数
    """
    name: str = Field(default='', max_length=100)  # 小程序名称
    primary_id: str = Field(default='', alias='primaryId', max_length=100)  # 原始ID
    app_id: str = Field(default='', alias='appId', max_length=100)  # appId
    app_secret: str = Field(default='', alias='appSecret', max_length=200)  # appSecret
    qr_code: str = Field(default='', alias='qrCode', max_length=300)  # 小程序码
    url: str = Field(default='', max_length=300)  # URL
    token: str = Field(default='', max_length=200)  # Token
    encoding_aes_key: str = Field(default='', alias='encodingAesKey', max_length=43)  # EncodingAESKey
    encryption_type: Literal[1, 2, 3] = Field(default=1, alias='encryptionType')  # EncryptionType


class ChannelOaSubMenus(BaseModel):
    """
    公众号单项子菜单
    """
    name: str = Field(default='', max_length=100)  # 菜单名称
    type: str = Field(default='', alias='visitType')  # miniprogram=小程序, view=网页
    url: str = Field(default='', max_length=100)  # 网址
    pagepath: str = Field(default='', alias='pagePath')  # 路径
    appid: str = Field(default='', alias='appId')  # 路径


class ChannelOaMenusItem(BaseModel):
    """
    公众号单项菜单
    """
    name: str = Field()  # 一级菜单名称
    menu_type: int = Field(alias='menuType')  # 菜单类型 1=没有子菜单, 2=有子菜单
    type: str = Field(default='', alias='visitType')  # miniprogram=小程序, view=网页
    sub_button: List[ChannelOaSubMenus] = Field(default=None, alias='subButtons')


class ChannelOaMenusIn(BaseModel):
    """
    公众号保存菜单参数
    """
    __root__: List[ChannelOaMenusItem]


class ChannelH5In(BaseModel):
    """
    H5渠道参数
    """
    status: Literal[0, 1] = Field(alias='status')  # 是否关闭
    close: Literal[0, 1] = Field(alias='close')  # 关闭类型
    url: str = Field(default='', max_length=500)  # 关闭访问URL
