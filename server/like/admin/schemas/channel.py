from typing import List, Union

from fastapi import Query
from pydantic import BaseModel, Field
from typing_extensions import Literal

from like.schema_base import EmptyStrToNone


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


class ChannelMpIn(BaseModel):
    """
    小程序渠道参数
    """
    name: str = Field(default='', max_length=100)  # 小程序名称
    primary_id: str = Field(default='', alias='primaryId', max_length=100)  # 原始ID
    app_id: str = Field(default='', alias='appId', max_length=100)  # appId
    app_secret: str = Field(default='', alias='appSecret', max_length=200)  # appSecret
    qr_code: str = Field(default='', alias='qrCode', max_length=300)  # 小程序码


class ChannelWxIn(BaseModel):
    """
    开放平台渠道参数
    """
    app_id: str = Field(default='', alias='appId', max_length=100)  # appId
    app_secret: str = Field(default='', alias='appSecret', max_length=200)  # appSecret


class ChannelOaReplyDefaultDetailIn(BaseModel):
    """渠道公众号默认回复详情参数"""
    id: int = Query(gt=0)  # 主键


class ChannelOaReplyDefaultCreateIn(BaseModel):
    """渠道公众号默认回复参数"""
    name: str  # 规则名称
    content: str  # 回复内容
    content_type: Literal[1, 2] = Field(alias='contentType')  # 内容类型
    matching_type: Union[Literal[1, 2], None] = Field(default=1, alias='matchingType')  # 匹配方式
    status: Literal[0, 1]  # 状态


class ChannelOaReplyDefaultEditIn(ChannelOaReplyDefaultCreateIn):
    """渠道公众号默认回复参数"""
    id: int = Field(gt=0)  # 主键


class ChannelOaReplyOut(BaseModel):
    """渠道公众号回复返回信息"""
    id: int  # 主键
    name: str  # 规则名称
    keyword: str  # 关键词
    content: str  # 回复内容
    replyType: int = Field(alias='reply_type')  # 回复类型
    contentType: int = Field(alias='content_type')  # 内容类型
    matchingType: int = Field(alias='matching_type')  # 匹配方式
    sort: int  # sort
    status: int  # 状态

    class Config:
        orm_mode = True
