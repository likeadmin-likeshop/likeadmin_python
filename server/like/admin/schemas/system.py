from datetime import datetime
from typing import List, Union

from fastapi import Query
from pydantic import BaseModel, Field


class SystemLoginIn(BaseModel):
    """系统登录参数"""
    username: str = Field(min_length=2, max_length=20)  # 账号
    password: str = Field(min_length=6, max_length=32)  # 密码


class SystemLoginOut(BaseModel):
    """系统登录返回信息"""
    token: str  # 令牌


class SystemLogoutIn(BaseModel):
    """退出登录参数"""
    token: str  # 令牌


class SystemAuthAdminListIn(BaseModel):
    """管理员列表参数"""
    username: Union[str, None] = Query(default=None)  # 账号
    nickname: Union[str, None] = Query(default=None)  # 昵称
    role: Union[int, None] = Query(default=None)  # 角色ID


class SystemAuthAdminDetailIn(BaseModel):
    """管理员详情参数"""
    id: int = Query(gt=0)  # 主键


class SystemAuthAdminCreateIn(BaseModel):
    """管理员新增参数"""
    dept_id: int = Field(alias='deptId')  # 部门ID
    post_id: int = Field(alias='postId')  # 岗位ID
    username: str = Field(min_length=2, max_length=20)  # 账号
    nickname: str = Field(min_length=2, max_length=30)  # 昵称
    password: str  # 密码
    avatar: str  # 头像
    role: int = Field(gt=0)  # 角色
    sort: int = Field(ge=0)  # 排序
    is_disable: int = Field(alias='isDisable', ge=0, le=1)  # 是否禁用: [0=否, 1=是]
    is_multipoint: int = Field(alias='isMultipoint', ge=0, le=1)  # 多端登录: [0=否, 1=是]


class SystemAuthAdminEditIn(SystemAuthAdminCreateIn):
    """管理员编辑参数"""
    id: int = Field(gt=0)  # 主键


class SystemAuthAdminUpdateIn(BaseModel):
    """管理员更新参数"""
    avatar: str  # 头像
    nickname: str = Field(min_length=2, max_length=30)  # 昵称
    password: str  # 要修改的密码
    curr_password: str = Field(alias='currPassword', min_length=6, max_length=32)  # 当前密码


class SystemAuthAdminDelIn(BaseModel):
    """管理员删除参数"""
    id: int = Field(gt=0)  # 主键


class SystemAuthAdminDisableIn(BaseModel):
    """管理员状态切换参数"""
    id: int = Field(gt=0)  # 主键


class SystemAuthAdminOut(BaseModel):
    """管理员返回信息"""
    id: int  # 主键
    username: str  # 账号
    nickname: str  # 昵称
    avatar: str  # 头像
    role: Union[str, None]  # 角色
    deptId: int = Field(alias='dept_id')  # 部门ID
    postId: int = Field(alias='post_id')  # 岗位ID
    dept: Union[str, None]  # 部门
    isMultipoint: int = Field(alias='is_multipoint')  # 多端登录: [0=否, 1=是]
    isDisable: int = Field(alias='is_disable')  # 是否禁用: [0=否, 1=是]
    lastLoginIp: str = Field(alias='last_login_ip')  # 最后登录IP
    lastLoginTime: datetime = Field(alias='last_login_time')  # 最后登录时间
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True

    # def __init__(self, avatar, **kwargs):  #     super().__init__(avatar=avatar, **kwargs)


class SystemAuthAdminSelfOneOut(BaseModel):
    """当前管理员返回部分信息"""
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


class SystemAuthAdminSelfOut(BaseModel):
    """当前系统管理员返回信息"""
    user: SystemAuthAdminSelfOneOut  # 用户信息
    permissions: List[str]  # 权限集合: [[*]=>所有权限, ['article:add']=>部分权限]

    class Config:
        orm_mode = True


class SystemAuthRoleCreateIn(BaseModel):
    """新增角色参数"""
    name: str = Field(min_length=1, max_length=30)  # 角色名称
    sort: int = Field(ge=0)  # 角色排序
    is_disable: int = Field(alias='isDisable', ge=0, le=1)  # 是否禁用: [0=否, 1=是]
    remark: str = Field(default='', max_length=200)  # 角色备注
    menu_ids: Union[str, None] = Field(alias='menuIds')  # 关联菜单


class SystemAuthRoleEditIn(SystemAuthRoleCreateIn):
    """编辑角色参数"""
    id: int = Field(gt=0)  # 主键


class SystemAuthRoleOut(BaseModel):
    """系统角色返回信息"""
    id: int  # 主键
    name: str  # 角色名称
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True


class SystemAuthRoleDetailOut(SystemAuthRoleOut):
    """系统角色返回信息"""
    remark: str  # 角色备注
    menus: List[int]  # 关联菜单
    member: int  # 成员数量
    sort: int  # 角色排序
    isDisable: int = Field(alias='is_disable')  # 是否禁用: [0=否, 1=是]

    class Config:
        orm_mode = True


class SystemAuthPostOut(BaseModel):
    id: int
    code: str
    name: str
    remarks: str
    sort: int
    isStop: int = Field(alias='is_stop')
    createTime: str = Field(alias='create_time')
    updateTime: str = Field(alias='update_time')

    class Config:
        orm_mode = True
