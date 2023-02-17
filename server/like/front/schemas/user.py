from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class UserCenterOut(BaseModel):
    """个人中心返回"""
    id: int  # 主键
    sn: int  # 编号
    avatar: str  # 头像
    realName: str = Field(alias='real_name')  # 真实姓名
    nickname: str  # 用户昵称
    username: str  # 用户账号
    mobile: str  # 用户电话

    class Config:
        orm_mode = True


class UserInfoOut(UserCenterOut):
    """个人信息返回"""
    sex: str  # 用户性别
    isPassword: Union[bool, None] = Field(alias='is_password')  # 用户性别
    isBindMnp: Union[bool, None] = Field(alias='is_bind_mnp')  # 用户性别
    version: Union[str, None]  # 版本
    createTime: datetime = Field(alias='create_time')  # 创建时间

    class Config:
        orm_mode = True
