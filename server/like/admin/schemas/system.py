from datetime import date, datetime
from typing import List, Union

from fastapi import Query
from pydantic import BaseModel, Field
from typing_extensions import Literal

from like.schema_base import EmptyStrToNone


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
    role: Union[int, None, EmptyStrToNone] = Query(default=None)  # 角色ID


class SystemAuthAdminDetailIn(BaseModel):
    """管理员详情参数"""
    id: int = Query(gt=0)  # 主键


class SystemAuthAdminCreateIn(BaseModel):
    """管理员新增参数"""
    role_ids: List[int] = Field(alias='roleIds')  # 角色ID
    dept_ids: List[int] = Field(alias='deptIds')  # 部门ID
    post_ids: List[int] = Field(alias='postIds')  # 岗位ID
    username: str = Field(min_length=2, max_length=20)  # 账号
    nickname: str = Field(min_length=2, max_length=30)  # 昵称
    password: str  # 密码
    avatar: str  # 头像
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


class SystemAuthAdminDetailOut(BaseModel):
    """管理员详情返回信息"""
    id: int  # 主键
    username: str  # 账号
    nickname: str  # 昵称
    avatar: str  # 头像
    roleIds: Union[List[int], str] = Field(alias='role_ids')  # 角色
    deptIds: Union[List[int], str] = Field(alias='dept_ids')  # 部门
    postIds: Union[List[int], str] = Field(alias='post_ids')  # 岗位
    isMultipoint: int = Field(alias='is_multipoint')  # 多端登录: [0=否, 1=是]
    isDisable: int = Field(alias='is_disable')  # 是否禁用: [0=否, 1=是]
    lastLoginIp: str = Field(alias='last_login_ip')  # 最后登录IP
    lastLoginTime: datetime = Field(alias='last_login_time')  # 最后登录时间
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间

    class Config:
        orm_mode = True


class SystemAuthAdminSelfOneOut(BaseModel):
    """当前管理员返回部分信息"""
    id: int  # 主键
    username: str  # 账号
    nickname: str  # 昵称
    avatar: str  # 头像
    # role: str  # 角色
    # dept: str = Field(alias='dept_id')  # 部门
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


class SystemAuthRoleDetailIn(BaseModel):
    """角色详情参数"""
    id: int = Query(gt=0)  # 主键


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


class SystemAuthRoleDelIn(BaseModel):
    """删除角色参数"""
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
    menus: List[int] = Field(default_factory=list)  # 关联菜单
    member: int = Field(default=0)  # 成员数量
    sort: int  # 角色排序
    isDisable: int = Field(alias='is_disable')  # 是否禁用: [0=否, 1=是]

    class Config:
        orm_mode = True


class SystemAuthMenuDetailIn(BaseModel):
    """菜单详情参数"""
    id: int = Query(gt=0)  # 主键


class SystemAuthMenuCreateIn(BaseModel):
    """新增菜单参数"""
    pid: int = Field(ge=0)  # 上级菜单
    menu_type: Literal['M', 'C', 'A'] = Field(alias='menuType')  # 权限类型: [M=目录, C=菜单, A=按钮]
    menu_name: str = Field(alias='menuName', min_length=1, max_length=30)  # 菜单名称
    menu_icon: Union[str, None] = Field(alias='menuIcon', max_length=100)  # 菜单图标
    menu_sort: int = Field(alias='menuSort', ge=0)  # 菜单排序
    perms: Union[str, None] = Field(max_length=100)  # 权限标识
    paths: Union[str, None] = Field(max_length=200)  # 路由地址
    component: Union[str, None] = Field(max_length=200)  # 前端组件
    selected: Union[str, None] = Field(max_length=200)  # 选中路径
    params: Union[str, None] = Field(max_length=200)  # 路由参数
    is_cache: int = Field(alias='isCache', ge=0, le=1)  # 是否缓存: [0=否, 1=是]
    is_show: int = Field(alias='isShow', ge=0, le=1)  # 是否显示: [0=否, 1=是]
    is_disable: int = Field(alias='isDisable', ge=0, le=1)  # 是否禁用: [0=否, 1=是]


class SystemAuthMenuEditIn(SystemAuthMenuCreateIn):
    """编辑菜单参数"""
    id: int = Field(gt=0)  # 主键


class SystemAuthMenuDelIn(BaseModel):
    """删除菜单参数"""
    id: int = Field(gt=0)  # 主键


class SystemAuthMenuOut(BaseModel):
    """系统菜单返回信息"""
    id: int  # 主键
    pid: int  # 上级菜单
    menuType: str = Field(alias='menu_type')  # 权限类型: [M=目录, C=菜单, A=按钮]
    menuName: str = Field(alias='menu_name')  # 菜单名称
    menuIcon: str = Field(alias='menu_icon')  # 菜单图标
    menuSort: int = Field(alias='menu_sort')  # 菜单排序
    perms: str  # 权限标识
    paths: str  # 路由地址
    component: str  # 前端组件
    selected: str  # 选中路径
    params: str  # 路由参数
    isCache: int = Field(alias='is_cache')  # 是否缓存: [0=否, 1=是]
    isShow: int = Field(alias='is_show')  # 是否显示: [0=否, 1=是]
    isDisable: int = Field(alias='is_disable')  # 是否禁用: [0=否, 1=是]
    createTime: datetime = Field(alias='create_time')  # 创建时间
    updateTime: datetime = Field(alias='update_time')  # 更新时间
    children: Union['SystemAuthMenuOut', None]  # 子集

    class Config:
        orm_mode = True


class SystemAuthPostOut(BaseModel):
    """
    系统岗位返回信息
    """
    id: int
    code: str
    name: str
    remarks: str
    sort: int
    isStop: int = Field(alias='is_stop')
    createTime: datetime = Field(alias='create_time')
    updateTime: datetime = Field(alias='update_time')

    class Config:
        orm_mode = True


class SystemAuthPostAddIn(BaseModel):
    """
    系统岗位新增参数
    """
    code: str
    name: str
    remarks: str
    sort: int
    is_stop: int = Field(alias='isStop')


class SystemAuthPostEditIn(SystemAuthPostAddIn):
    """
    系统岗位编辑参数
    """
    id: int = Field(gt=0)  # 主键


class SystemAuthPostDelIn(BaseModel):
    """
    系统岗位删除参数
    """
    id: int = Field(gt=0)  # 主键


class SystemAuthPostDetailIn(BaseModel):
    """
    系统岗位详情参数
    """
    id: int = Query(gt=0)  # 主键


class SystemAuthDeptOut(BaseModel):
    """
    系统部门返回信息
    """
    id: int
    pid: int  # 上级ID
    name: str  # 部门名称
    duty: str  # 负责人名
    mobile: str  # 联系电话
    sort: int  # 部门排序
    isStop: int = Field(alias='is_stop')
    createTime: datetime = Field(alias='create_time')
    updateTime: datetime = Field(alias='update_time')

    class Config:
        orm_mode = True


class SystemAuthDeptDetailIn(BaseModel):
    id: int = Query(gt=0)  # 主键


class SystemAuthDeptDeleteIn(BaseModel):
    id: int = Query(gt=0)  # 主键


class SystemAuthDeptAddIn(BaseModel):
    pid: int  # 上级ID
    name: str  # 部门名称
    duty: str  # 负责人名
    mobile: str  # 联系电话
    sort: int  # 部门排序
    is_stop: int = Field(alias='isStop')


class SystemAuthDeptListIn(BaseModel):
    isStop: Union[int, None, EmptyStrToNone] = Query(default=None)
    name: Union[str, None] = Query(default=None)


class SystemAuthDeptEditIn(SystemAuthDeptAddIn):
    id: int = Query(gt=0)  # 主键


class SystemLogOperateIn(BaseModel):
    """操作日志列表参数"""
    title: Union[str, None] = Query(default=None)  # 操作标题
    username: Union[str, None] = Query(default=None)  # 用户账号
    ip: Union[str, None] = Query(default=None)  # 请求IP
    type: Union[str, None] = Query(default=None)  # 请求类型: GET/POST/PUT
    status: Union[int, None, EmptyStrToNone] = Query(default=None)  # 执行状态: [1=成功, 2=失败]
    url: Union[str, None] = Query(default=None)  # 请求地址
    start_time: Union[date, None, EmptyStrToNone] = Query(alias='startTime')  # 开始时间
    end_time: Union[date, None, EmptyStrToNone] = Query(alias='endTime')  # 结束时间


class SystemLogOperateOut(BaseModel):
    """操作日志返回信息"""
    id: int  # 主键
    username: str  # 用户账号
    nickname: str  # 用户昵称
    type: str  # 请求类型: GET/POST/PUT
    title: str  # 操作标题
    method: str  # 请求方式
    ip: str  # 请求IP
    url: str  # 请求地址
    args: str  # 请求参数
    error: str  # 错误信息
    status: int  # 执行状态: [1=成功, 2=失败]
    taskTime: str = Field(alias='task_time')  # 执行耗时
    startTime: datetime = Field(alias='start_time')  # 开始时间
    endTime: datetime = Field(alias='end_time')  # 结束时间
    createTime: datetime = Field(alias='create_time')  # 创建时间

    class Config:
        orm_mode = True


class SystemLogLoginIn(BaseModel):
    """登录日志列表参数"""
    username: Union[str, None] = Query(default=None)  # 登录账号
    status: Union[int, None, EmptyStrToNone] = Query(default=None)  # 操作状态: [1=成功, 2=失败]
    start_time: Union[date, None, EmptyStrToNone] = Query(alias='startTime')  # 开始时间
    end_time: Union[date, None, EmptyStrToNone] = Query(alias='endTime')  # 结束时间


class SystemLogLoginOut(BaseModel):
    """登录日志返回信息"""
    id: int  # 主键
    username: str  # 登录账号
    ip: str  # 来源IP
    os: str  # 操作系统
    browser: str  # 浏览器
    status: int  # 操作状态: [1=成功, 2=失败]
    createTime: datetime = Field(alias='create_time')  # 创建时间

    class Config:
        orm_mode = True
