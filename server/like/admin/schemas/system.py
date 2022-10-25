from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class SystemLoginIn(BaseModel):
    """系统登录参数"""
    username: str
    password: str


class SystemLoginOut(BaseModel):
    """系统登录返回信息"""
    token: str


class SystemLogoutIn(BaseModel):
    """退出登录参数"""
    token: str


class SystemAuthAdminOut(BaseModel):
    """管理员返回信息"""
    id: int  # 主键
    username: str  # 账号
    nickname: str  # 昵称
    avatar: str  # 头像
    role: str  # 角色
    dept: str = Field(alias='dept_id')  # 部门
    isMultipoint: int = Field(alias='is_multipoint')  # 多端登录: [0=否, 1=是]
    isDisable: int = Field(alias='is_disable')  # 是否禁用: [0=否, 1=是]
    lastLoginIp: str = Field(alias='last_login_ip')  # 最后登录IP
    lastLoginTime: datetime = Field(alias='last_login_time')  # 最后登录时间
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    # def __init__(self, avatar, **kwargs):
    #     super().__init__(avatar=avatar, **kwargs)


class SystemAuthAdminSelfOut(BaseModel):
    """当前系统管理员返回信息"""
    user: SystemAuthAdminOut  # 用户信息
    permissions: List[str]  # 权限集合: [[*]=>所有权限, ['article:add']=>部分权限]
