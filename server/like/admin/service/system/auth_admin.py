import json
import time
from abc import ABC, abstractmethod
from typing import Union

from fastapi import Depends, Request
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.admin.config import AdminConfig
from like.admin.schemas.system import (
    SystemAuthAdminCreateIn, SystemAuthAdminEditIn, SystemAuthAdminUpdateIn, SystemAuthAdminListIn,
    SystemAuthAdminOut, SystemAuthAdminSelfOneOut, SystemAuthAdminSelfOut, SystemAuthAdminDetailOut)
from like.dependencies.database import db
from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.models import (
    system_auth_admin, system_auth_menu, system_auth_role, system_auth_dept, SystemAuthAdmin)
from like.utils.redis import RedisUtil
from like.utils.tools import ToolsUtil
from like.utils.urls import UrlUtil
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
            menu_ids = await self.auth_perm_service.select_menu_ids_by_role_id([int(i) for i in sys_admin.role_ids.split(',')])
            if menu_ids:
                menus = await db.fetch_all(
                    system_auth_menu.select()
                    .where(system_auth_menu.c.id.in_(menu_ids), system_auth_menu.c.is_disable == 0,
                           system_auth_menu.c.menu_type.in_(['C', 'A']))
                    .order_by(system_auth_menu.c.menu_sort, system_auth_menu.c.id))
                if menus:
                    auths.extend((i.perms.strip() for i in menus if i))
            if not auths:
                auths.append('')
        else:
            auths.append('*')
        admin = SystemAuthAdminSelfOneOut.from_orm(sys_admin)
        admin.avatar = await UrlUtil.to_absolute_url(admin.avatar)
        return SystemAuthAdminSelfOut(user=admin, permissions=auths)

    async def list(self, list_in: SystemAuthAdminListIn) -> AbstractPage[SystemAuthAdminOut]:
        """管理员列表"""
        columns = [system_auth_admin.c.id,
                   system_auth_admin.c.dept_ids.label('dept'), system_auth_admin.c.role_ids.label('role'),
                   system_auth_admin.c.username, system_auth_admin.c.nickname, system_auth_admin.c.avatar,
                   system_auth_admin.c.is_multipoint, system_auth_admin.c.is_disable,
                   system_auth_admin.c.last_login_ip, system_auth_admin.c.last_login_time,
                   system_auth_admin.c.create_time, system_auth_admin.c.update_time]
        # 查询条件
        where = [system_auth_admin.c.is_delete == 0]
        if list_in.username:
            where.append(system_auth_admin.c.username.like(f'%{list_in.username}%'))
        if list_in.nickname:
            where.append(system_auth_admin.c.nickname.like(f'%{list_in.nickname}%'))
        if list_in.role is not None:
            where.append(system_auth_admin.c.role.in_(list_in.role))
        query = select(columns).where(*where) \
            .select_from(system_auth_admin) \
            .order_by(system_auth_admin.c.id.desc(), system_auth_admin.c.sort.desc())
        pager = await paginate(db, query)
        # 处理返回结果
        for obj in pager.lists:
            obj.avatar = await UrlUtil.to_absolute_url(obj.avatar)
            if obj.id == 1:
                obj.role = '系统管理员'
            else:
                role_ids = [int(i) for i in obj.role.split(',') if i.isdigit()]
                roles = await db.fetch_all(system_auth_role.select().where(system_auth_role.c.id.in_(role_ids)))
                obj.role = '/'.join([i.name for i in roles])
            if not obj.dept:
                obj.dept = ''
            else:
                dept_ids = [int(i) for i in obj.dept.split(',') if i.isdigit()]
                depts = await db.fetch_all(system_auth_dept.select().where(
                    system_auth_dept.c.id.in_(dept_ids), system_auth_dept.c.is_delete == 0))
                obj.dept = '/'.join([i.name for i in depts])
        return pager

    async def detail(self, id_: int) -> SystemAuthAdminDetailOut:
        """管理员详细"""
        sys_admin = await db.fetch_one(
            system_auth_admin.select().where(
                system_auth_admin.c.id == id_, system_auth_admin.c.is_delete == 0).limit(1))
        assert sys_admin, '账号已不存在！'
        sys_admin_out = SystemAuthAdminDetailOut.from_orm(sys_admin)
        sys_admin_out.avatar = await UrlUtil.to_absolute_url(sys_admin_out.avatar)
        sys_admin_out.roleIds = [int(i) for i in sys_admin_out.roleIds.split(',') if i.isdigit()]
        sys_admin_out.deptIds = [int(i) for i in sys_admin_out.deptIds.split(',') if i.isdigit()]
        sys_admin_out.postIds = [int(i) for i in sys_admin_out.postIds.split(',') if i.isdigit()]
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
        if not (6 <= len(admin_create_in.password) <= 20):
            raise AppException(HttpResp.FAILED, msg='密码必须在6~20位')
        create_dict = dict(admin_create_in)
        salt = ToolsUtil.random_string(5)
        create_dict['role_ids'] = ','.join([str(i) for i in admin_create_in.role_ids])
        create_dict['dept_ids'] = ','.join([str(i) for i in admin_create_in.dept_ids])
        create_dict['post_ids'] = ','.join([str(i) for i in admin_create_in.post_ids])
        create_dict['salt'] = salt
        create_dict['password'] = ToolsUtil.make_md5(f'{admin_create_in.password.strip()}{salt}')
        create_dict['avatar'] = await UrlUtil.to_relative_url(admin_create_in.avatar) \
            if admin_create_in.avatar else '/api/static/backend_avatar.png'
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(system_auth_admin.insert().values(**create_dict))

    async def edit(self, admin_edit_in: SystemAuthAdminEditIn):
        """管理员编辑"""
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
        # 更新管理员信息
        admin_dict = admin_edit_in.dict()
        admin_dict['role_ids'] = ','.join([str(i) for i in admin_edit_in.role_ids])
        admin_dict['dept_ids'] = ','.join([str(i) for i in admin_edit_in.dept_ids])
        admin_dict['post_ids'] = ','.join([str(i) for i in admin_edit_in.post_ids])
        admin_dict['avatar'] = await UrlUtil.to_relative_url(admin_edit_in.avatar)
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
        await self.cache_admin_user_by_uid(admin_edit_in.id)
        # 如果更改自己的密码,则删除旧缓存
        id_ = self.request.state.admin_id
        if admin_edit_in.password and admin_edit_in.id == id_:
            token = self.request.headers.get('token', '')
            await RedisUtil.delete(f'{AdminConfig.backstage_token_key}{token}')
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
        admin_dict['avatar'] = await UrlUtil.to_relative_url(admin_update_in.avatar) \
            if admin_update_in.avatar else '/api/static/backend_avatar.png'
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
        await self.cache_admin_user_by_uid(admin_id)
        # 如果更改自己的密码,则删除旧缓存
        id_ = admin_id
        if admin_update_in.password:
            token = self.request.headers.get('token', '')
            await RedisUtil.delete(f'{AdminConfig.backstage_token_key}{token}')
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
        self.request: Request = request
        self.auth_perm_service: ISystemAuthPermService = auth_perm_service
        self.auth_role_service: ISystemAuthRoleService = auth_role_service

    @classmethod
    async def instance(cls, request: Request,
                       auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance),
                       auth_role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
        """实例化"""
        return cls(request, auth_perm_service, auth_role_service)
