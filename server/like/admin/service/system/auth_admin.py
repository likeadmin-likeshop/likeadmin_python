import json
import time
from abc import ABC, abstractmethod
from typing import Union, Final

from sqlalchemy import select
from fastapi import Depends, Request
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate

from like.admin.config import AdminConfig
from like.admin.schemas.system import (
    SystemAuthAdminCreateIn, SystemAuthAdminEditIn, SystemAuthAdminUpdateIn, SystemAuthAdminListIn,
    SystemAuthAdminOut, SystemAuthAdminSelfOneOut, SystemAuthAdminSelfOut)
from like.dependencies.database import db
from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.models import (
    system_auth_admin, system_auth_menu, system_auth_role, system_auth_dept, SystemAuthAdmin)
from like.utils.redis import RedisUtil
from like.utils.tools import ToolsUtil
from .auth_perm import ISystemAuthPermService, SystemAuthPermService
from .auth_role import ISystemAuthRoleService, SystemAuthRoleService


class ISystemAuthAdminService(ABC):
    """系统管理员服务抽象类"""

    @abstractmethod
    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        pass

    @abstractmethod
    async def self(self, admin_id: int) -> SystemAuthAdminSelfOut:
        pass

    @abstractmethod
    async def list(self, list_in: SystemAuthAdminListIn) -> AbstractPage[SystemAuthAdminOut]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> SystemAuthAdminOut:
        pass

    @abstractmethod
    async def add(self, admin_create_in: SystemAuthAdminCreateIn):
        pass

    @abstractmethod
    async def edit(self, admin_edit_in: SystemAuthAdminEditIn):
        pass

    @abstractmethod
    async def update(self, admin_update_in: SystemAuthAdminUpdateIn, admin_id: int):
        pass

    @abstractmethod
    async def delete(self, id_: int):
        pass

    @abstractmethod
    async def disable(self, id_: int):
        pass

    @classmethod
    @abstractmethod
    async def cache_admin_user_by_uid(cls, id_: int):
        pass


class SystemAuthAdminService(ISystemAuthAdminService):
    """系统管理员服务实现类"""

    async def find_by_username(self, username: str) -> Union[SystemAuthAdmin, None]:
        """根据账号查找管理员"""
        row = await db.fetch_one(
            system_auth_admin.select().where(system_auth_admin.c.username == username).limit(1))
        return SystemAuthAdmin(**row) if row else None

    async def self(self, admin_id: int) -> SystemAuthAdminSelfOut:
        """当前管理员"""
        # 管理员信息
        sys_admin = await db.fetch_one(
            system_auth_admin.select().where(
                system_auth_admin.c.id == admin_id, system_auth_admin.c.is_delete == 0).limit(1))
        # 角色权限
        auths = []
        if admin_id > 1:
            menu_ids = self.auth_perm_service.select_menu_ids_by_role_id(int(sys_admin.role))
            if menu_ids:
                menus = await db.fetch_all(
                    system_auth_menu.select()
                    .where(system_auth_menu.c.id == menu_ids, system_auth_menu.c.is_disable == 0,
                           system_auth_menu.c.menu_type.in_['C', 'A'])
                    .order_by(system_auth_menu.c.menu_sort, system_auth_menu.c.id))
                if menus:
                    auths.extend((i.perms.strip() for i in menus if i))
            if not auths:
                auths.append('')
        else:
            auths.append('*')
        # TODO: 头像路径处理
        return SystemAuthAdminSelfOut(user=SystemAuthAdminSelfOneOut.from_orm(sys_admin), permissions=auths)

    async def list(self, list_in: SystemAuthAdminListIn) -> AbstractPage[SystemAuthAdminOut]:
        """管理员列表"""
        columns = [system_auth_admin.c.id, system_auth_admin.c.dept_id, system_auth_admin.c.post_id,
                   system_auth_admin.c.username, system_auth_admin.c.nickname, system_auth_admin.c.avatar,
                   system_auth_dept.c.name.label('dept'), system_auth_role.c.name.label('role'),
                   system_auth_admin.c.is_multipoint, system_auth_admin.c.is_disable,
                   system_auth_admin.c.last_login_ip, system_auth_admin.c.last_login_time,
                   system_auth_admin.c.create_time, system_auth_admin.c.update_time]
        # 查询条件
        where = [system_auth_admin.c.is_delete == 0]
        if list_in.username:
            where.append(system_auth_admin.c.username.like(f'%{list_in.username}%'))
        if list_in.nickname:
            where.append(system_auth_admin.c.nickname.like(f'%{list_in.nickname}%'))
        if list_in.role:
            where.append(system_auth_admin.c.role == list_in.role)
        query = select(columns).where(*where) \
            .select_from(
            system_auth_admin.outerjoin(system_auth_role, system_auth_admin.c.role == system_auth_role.c.id)
            .outerjoin(system_auth_dept, system_auth_admin.c.dept_id == system_auth_dept.c.id)) \
            .order_by(system_auth_admin.c.id.desc(), system_auth_admin.c.sort.desc())
        pager = await paginate(db, query)
        # 处理返回结果
        for obj in pager.lists:
            # TODO: 头像路径处理
            if obj.id == 1:
                obj.role = '系统管理员'
            if not obj.dept:
                obj.dept = ''
        return pager

    async def detail(self, id_: int) -> SystemAuthAdminOut:
        """管理员详细"""
        sys_admin = await db.fetch_one(
            system_auth_admin.select().where(
                system_auth_admin.c.id == id_, system_auth_admin.c.is_delete == 0).limit(1))
        assert sys_admin, '账号已不存在！'
        # TODO: 头像路径处理
        sys_admin_out = SystemAuthAdminOut.from_orm(sys_admin)
        if not sys_admin_out.dept:
            sys_admin_out.dept = str(sys_admin_out.deptId)
        return sys_admin_out

    async def add(self, admin_create_in: SystemAuthAdminCreateIn):
        """管理员新增"""
        assert not await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.username == admin_create_in.username,
                   system_auth_admin.c.is_delete == 0).limit(1)), '账号已存在换一个吧！'
        assert not await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.nickname == admin_create_in.nickname,
                   system_auth_admin.c.is_delete == 0).limit(1)), '昵称已存在换一个吧！'
        role_out = await self.auth_role_service.detail(admin_create_in.role)
        assert role_out, '角色不存在!'
        assert role_out.isDisable <= 0, '当前角色已被禁用!'
        create_dict = dict(admin_create_in)
        salt = ToolsUtil.random_string(5)
        create_dict['salt'] = salt
        create_dict['password'] = ToolsUtil.make_md5(f'{admin_create_in.password.strip()}{salt}')
        # TODO: 头像路径处理
        create_dict['avatar'] = admin_create_in.avatar if admin_create_in.avatar else '/api/static/backend_avatar.png'
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(system_auth_admin.insert().values(**create_dict))

    async def edit(self, admin_edit_in: SystemAuthAdminEditIn):
        """管理员更新"""
        assert await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.id == admin_edit_in.id, system_auth_admin.c.is_delete == 0)
            .limit(1)), '账号不存在了!'
        assert not await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.username == admin_edit_in.username,
                   system_auth_admin.c.is_delete == 0,
                   system_auth_admin.c.id != admin_edit_in.id)
            .limit(1)), '账号已存在换一个吧！'
        assert not await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.nickname == admin_edit_in.nickname,
                   system_auth_admin.c.is_delete == 0,
                   system_auth_admin.c.id != admin_edit_in.id)
            .limit(1)), '昵称已存在换一个吧！'
        if admin_edit_in.role > 0 and admin_edit_in.id != 1:
            assert await self.auth_role_service.detail(admin_edit_in.role), '角色不存在!'
        # 更新管理员信息
        admin_dict = admin_edit_in.dict()
        # TODO: 头像路径处理
        admin_dict['avatar'] = admin_edit_in.avatar
        admin_dict['role'] = 0 if admin_edit_in.id == 1 else admin_edit_in.role
        admin_dict['update_time'] = int(time.time())
        if admin_edit_in.id == 1:
            del admin_dict['username']
        if admin_edit_in.password:
            if not (6 <= len(admin_edit_in.password) <= 20):
                raise AppException(HttpResp.FAILED, msg='密码必须在6~20位')
            salt = ToolsUtil.random_string(5)
            admin_dict['salt'] = salt
            admin_dict['password'] = ToolsUtil.make_md5(f'{admin_edit_in.password.strip()}{salt}')
        else:
            del admin_dict['password']
        await db.execute(system_auth_admin.update()
                         .where(system_auth_admin.c.id == admin_edit_in.id)
                         .values(**admin_dict))
        self.cache_admin_user_by_uid(admin_edit_in.id)
        # 如果更改自己的密码,则删除旧缓存
        id_ = self.request.state.admin_id
        if admin_edit_in.password and admin_edit_in.id == id_:
            token = self.request.headers.get('token', '')
            RedisUtil.delete(f'{AdminConfig.backstage_token_key}{token}')
            sys_admin_set_key = f'{AdminConfig.backstage_token_set}{id_}'
            ts = await RedisUtil.sget(sys_admin_set_key)
            if ts:
                await RedisUtil.delete(*(f'{AdminConfig.backstage_token_key}{t}' for t in ts))
            await RedisUtil.delete(sys_admin_set_key)
            await RedisUtil.sset(sys_admin_set_key, token)

    async def update(self, admin_update_in: SystemAuthAdminUpdateIn, admin_id: int):
        """管理员更新"""
        sys_admin = await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.id == admin_id,
                   system_auth_admin.c.is_delete == 0).limit(1))
        assert sys_admin, '账号不存在了!'
        # 更新管理员信息
        admin_dict = admin_update_in.dict()
        del admin_dict['curr_password']
        # TODO: 头像路径处理
        admin_dict['avatar'] = admin_update_in.avatar if admin_update_in.avatar else '/api/static/backend_avatar.png'
        admin_dict['update_time'] = int(time.time())
        if admin_update_in.password:
            curr_pass = ToolsUtil.make_md5(f'{admin_update_in.curr_password}{sys_admin.salt}')
            if curr_pass != sys_admin.password:
                raise AppException(HttpResp.FAILED, msg='当前密码不正确!')
            if not (6 <= len(admin_update_in.password) <= 20):
                raise AppException(HttpResp.FAILED, msg='密码必须在6~20位')
            salt = ToolsUtil.random_string(5)
            admin_dict['salt'] = salt
            admin_dict['password'] = ToolsUtil.make_md5(f'{admin_update_in.password.strip()}{salt}')
        else:
            del admin_dict['password']
        await db.execute(system_auth_admin.update()
                         .where(system_auth_admin.c.id == sys_admin.id)
                         .values(**admin_dict))
        self.cache_admin_user_by_uid(admin_id)
        # 如果更改自己的密码,则删除旧缓存
        id_ = admin_id
        if admin_update_in.password:
            token = self.request.headers.get('token', '')
            RedisUtil.delete(f'{AdminConfig.backstage_token_key}{token}')
            sys_admin_set_key = f'{AdminConfig.backstage_token_set}{id_}'
            ts = await RedisUtil.sget(sys_admin_set_key)
            if ts:
                await RedisUtil.delete(*(f'{AdminConfig.backstage_token_key}{t}' for t in ts))
            await RedisUtil.delete(sys_admin_set_key)
            await RedisUtil.sset(sys_admin_set_key, token)

    async def delete(self, id_: int):
        """管理员删除"""
        assert await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.id == id_, system_auth_admin.c.is_delete == 0)
            .limit(1)), '账号已不存在!'
        assert id_ != 1, '系统管理员不允许删除!'
        assert id_ != self.request.state.admin_id, '不能删除自己!'
        await db.execute(system_auth_admin.update()
                         .where(system_auth_admin.c.id == id_)
                         .values(is_delete=1, delete_time=int(time.time())))
        await self.cache_admin_user_by_uid(id_)

    async def disable(self, id_: int):
        """管理员状态切换"""
        auth_admin = await db.fetch_one(
            system_auth_admin.select()
            .where(system_auth_admin.c.id == id_, system_auth_admin.c.is_delete == 0)
            .limit(1))
        assert auth_admin, '账号已不存在!'
        assert id_ != self.request.state.admin_id, '不能禁用自己!'
        await db.execute(system_auth_admin.update()
                         .where(system_auth_admin.c.id == id_)
                         .values(is_disable=1 if auth_admin.is_disable == 0 else 0,
                                 update_time=int(time.time())))

    @classmethod
    async def cache_admin_user_by_uid(cls, id_: int):
        """缓存管理员"""
        row = await db.fetch_one(
            system_auth_admin.select().where(system_auth_admin.c.id == id_).limit(1))
        await RedisUtil.hmset(f'{AdminConfig.backstage_manage_key}', {f'{row.id}': json.dumps(dict(row))})
        return

    def __init__(self, request: Request, auth_perm_service: ISystemAuthPermService,
                 auth_role_service: ISystemAuthRoleService):
        self.request: Final[Request] = request
        self.auth_perm_service: Final[ISystemAuthPermService] = auth_perm_service
        self.auth_role_service: Final[ISystemAuthRoleService] = auth_role_service

    @classmethod
    async def instance(cls, request: Request,
                       auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance),
                       auth_role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
        """实例化"""
        return cls(request, auth_perm_service, auth_role_service)
