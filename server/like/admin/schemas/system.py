from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class SystemLoginIn(BaseModel):
    """系统登录参数"""
    username: str  # 账号
    password: str  # 密码


class SystemLoginOut(BaseModel):
    """系统登录返回信息"""
    token: str  # 令牌


class SystemLogoutIn(BaseModel):
    """退出登录参数"""
    token: str  # 令牌


class SystemAuthAdminDetailIn(BaseModel):
    """管理员详情参数"""
    id: int  # 主键


class SystemAuthAdminCreateIn(BaseModel):
    """管理员新增参数"""
    dept_id: int = Field(alias='deptId')  # 部门ID
    post_id: int = Field(alias='postId')  # 岗位ID
    username: str  # 账号
    nickname: str  # 昵称
    password: str  # 密码
    avatar: str  # 头像
    role: int  # 角色
    sort: int  # 排序
    is_disable: int = Field(alias='isDisable')  # 是否禁用: [0=否, 1=是]
    is_multipoint: int = Field(alias='isMultipoint')  # 多端登录: [0=否, 1=是]


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

    class Config:
        orm_mode = True

    # def __init__(self, avatar, **kwargs):
    #     super().__init__(avatar=avatar, **kwargs)


class SystemAuthAdminSelfOut(BaseModel):
    """当前系统管理员返回信息"""
    user: SystemAuthAdminOut  # 用户信息
    permissions: List[str]  # 权限集合: [[*]=>所有权限, ['article:add']=>部分权限]

    class Config:
        orm_mode = True


class SystemAuthRoleOut(BaseModel):
    """系统角色返回信息"""
    id: int  # 主键
    name: str  # 角色名称
    remark: str  # 角色备注
    menus: List[int]  # 关联菜单
    member: int  # 成员数量
    sort: int  # 角色排序
    isDisable: int = Field(alias='is_disable')  # 是否禁用: [0=否, 1=是]
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True
