from datetime import date, datetime
from typing import Union

from fastapi import Query
from pydantic import BaseModel, Field

from like.common.enums import LoginClientEnum
from like.schema_base import EmptyStrToNone


class UserListIn(BaseModel):
    """用户列表参数"""
    keyword: str = Field(default='')  # 搜索关键词
    channel: Union[LoginClientEnum, None, EmptyStrToNone] = Field(
        default='')  # 客户端类型: [1=微信小程序, 2=微信公众号, 3=手机H5；4=电脑PC, 5=苹果APP, 6=安卓APP]
    start_time: Union[date, datetime, None, EmptyStrToNone] = Query(alias='startTime')  # 开始时间
    end_time: Union[date, datetime, None, EmptyStrToNone] = Query(alias='endTime')  # 结束时间


class UserDetailIn(BaseModel):
    """用户列表参数"""
    id: int = Query(gt=0)


class UserEditlIn(BaseModel):
    id: int = Query(gt=0)
    field: str
    value: str


class UserInfoOut(BaseModel):
    """
    用户信息输出
    """
    id: int  # 主键
    sn: int
    avatar: str
    realName: str = Field(alias='real_name')
    nickname: str
    username: str
    mobile: str
    sex: str
    channel: str
    lastLoginIp: str = Field(alias='last_login_ip')
    lastLoginTime: datetime = Field(alias='last_login_time')  # 最后登录时间
    createTime: datetime = Field(alias='create_time')  # 创建时间
