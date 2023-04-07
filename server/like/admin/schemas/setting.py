from datetime import datetime
from typing import List, Union

from fastapi import Query
from pydantic import BaseModel, Field
from typing_extensions import Literal

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
    name: str
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


class HotSearchItem(BaseModel):
    """
    热门搜索通用参数
    """
    name: str  # 关键词
    sort: int  # 排序号


class SettingHotSearchIn(BaseModel):
    """
    热门搜索参数
    """
    is_hot_search: Literal[0, 1] = Field(alias='isHotSearch')  # 是否开启搜索 0/1
    list: List[HotSearchItem]


class SettingHotSearchOut(BaseModel):
    """
    热门搜索返回
    """
    id: int
    name: str  # 关键词
    sort: int  # 排序号

    class Config:
        orm_mode = True


class SettingLoginIn(BaseModel):
    """
    登录设置保存参数
    """
    login_way: str = Field(default='', alias='loginWay')  # 登录方式, 逗号隔开
    force_bind_mobile: int = Field(default=0, alias='forceBindMobile')  # 强制绑定手机 0/1
    open_agreement: int = Field(default=0, alias='openAgreement')  # 是否开启协议 0/1
    open_other_auth: int = Field(default=0, alias='openOtherAuth')  # 第三方登录 0/1
    auto_login_auth: str = Field(default='', alias='autoLoginAuth')  # 第三方自动登录 逗号隔开


class SettingUserIn(BaseModel):
    """
    用户设置保存参数
    """
    default_avatar: str = Field(default='', alias='defaultAvatar')  # 默认头像


class SettingSmsDetailIn(BaseModel):
    """
    短信引擎详情参数
    """
    alias: str  # 别名


class SettingSmsSaveIn(BaseModel):
    """
    短信引擎保存参数
    """
    name: str  # 名称
    alias: str  # 别名
    status: Literal[0, 1]  # 状态
    sign: Union[str, None] = Field()
    appId: Union[str, None] = Field(alias='appId')
    appKey: Union[str, None] = Field(alias='appKey')
    secretId: Union[str, None] = Field(alias='secretId')
    secretKey: Union[str, None] = Field(alias='secretKey')


class SettingNoticeListIn(BaseModel):
    """
    通知设置列表参数
    """
    recipient: int = Query(ge=1, le=2)  # 类型: 1=用户, 2=平台


class SettingNoticeListOut(BaseModel):
    """
    通知设置列表返回
    """
    id: int
    name: str  # 场景名称
    type: str  # 通知类型: [1=业务, 2=验证]
    systemStatus: int = Field(default=0, alias='system_status')  # 系统的通知
    smsStatus: int = Field(default=0, alias='sms_status')  # 短信的通知
    oaStatus: int = Field(default=0, alias='oa_status')  # 公众号通知
    mnpStatus: int = Field(default=0, alias='mnp_status')  # 小程序通知
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True


class SettingNoticeDetailIn(BaseModel):
    """
    通知设置详情参数
    """
    id: int = Query(gt=0)  # 主键


class SettingNoticeDetailOut(BaseModel):
    """
    通知设置详情返回
    """
    id: int
    name: str  # 场景名称
    type: str  # 通知类型: [1=业务, 2=验证]
    remarks: str  # 场景描述
    systemNotice: dict = Field(default=0, alias='system_notice')  # 系统的通知
    smsNotice: dict = Field(default=0, alias='sms_notice')  # 短信的通知
    oaNotice: dict = Field(default=0, alias='oa_notice')  # 公众号通知
    mnpNotice: dict = Field(default=0, alias='mnp_notice')  # 小程序通知

    class Config:
        orm_mode = True


class SettingNoticeTpl(BaseModel):
    """
    通知设置项模板
    """
    tpl_name: Union[str, None] = Field(alias='tplName')
    tpl_keyword: Union[str, None] = Field(alias='tplKeyword')
    tpl_content: Union[str, None] = Field(alias='tplContent')


class SettingNoticeItem(BaseModel):
    """
    通知设置项
    """
    status: Union[Literal[0, 1, '0', '1'], None]  # 状态
    name: Union[str, None]  # 名称
    remark: Union[str, None]
    first: Union[str, None]
    title: Union[str, None]
    content: Union[str, None]
    template_id: Union[str, None] = Field(alias='templateId')
    template_sn: Union[str, None] = Field(alias='templateSn')
    tpl: Union[List[SettingNoticeTpl], None]


class SettingNoticeSaveIn(BaseModel):
    """
    通知设置保存参数
    """
    id: int
    system_notice: SettingNoticeItem = Field(alias='systemNotice')
    sms_notice: SettingNoticeItem = Field(alias='smsNotice')
    oa_notice: SettingNoticeItem = Field(alias='oaNotice')
    mnp_notice: SettingNoticeItem = Field(alias='mnpNotice')
