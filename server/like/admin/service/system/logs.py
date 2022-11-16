import time
from abc import ABC, abstractmethod
from typing import Final, List

import pydantic
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import func, select

from like.admin.config import AdminConfig
from like.admin.schemas.system import (SystemLogOperateIn, SystemLogLoginIn, SystemLogOperateOut, SystemLogLoginOut)
from like.dependencies.database import db
from like.models import system_log_operate, system_log_login, system_auth_admin


class ISystemLogsServer(ABC):
    """系统日志服务抽象类"""

    @abstractmethod
    async def operate(self, operate_in: SystemLogOperateIn) -> AbstractPage[SystemLogOperateOut]:
        pass

    @abstractmethod
    async def login(self, login_in: SystemLogLoginIn) -> AbstractPage[SystemLogLoginOut]:
        pass


class SystemLogsServer(ISystemLogsServer):
    """系统日志服务实现类"""

    async def operate(self, operate_in: SystemLogOperateIn) -> AbstractPage[SystemLogOperateOut]:
        """系统操作日志"""
        columns = [system_log_operate, system_auth_admin.c.username, system_auth_admin.c.nickname]
        # 查询条件
        where = []
        if operate_in.title:
            where.append(system_log_operate.c.title.like(f'%{operate_in.title}%'))
        if operate_in.username:
            where.append(system_auth_admin.c.username.like(f'%{operate_in.username}%'))
        if operate_in.ip:
            where.append(system_log_operate.c.ip.like(f'%{operate_in.ip}%'))
        if operate_in.type:
            where.append(system_log_operate.c.type == operate_in.type)
        if operate_in.status is not None:
            where.append(system_log_operate.c.status == operate_in.status)
        if operate_in.url:
            where.append(system_log_operate.c.url == operate_in.url)
        if operate_in.start_time:
            where.append(system_log_operate.c.create_time >= int(time.mktime(operate_in.start_time.timetuple())))
        if operate_in.end_time:
            where.append(system_log_operate.c.create_time <= int(time.mktime(operate_in.end_time.timetuple())))
        query = select(columns).where(*where) \
            .select_from(
            system_log_operate.outerjoin(
                system_auth_admin, system_log_operate.c.admin_id == system_auth_admin.c.id)) \
            .order_by(system_log_operate.c.id.desc())
        pager = await paginate(db, query)
        return pager

    async def login(self, login_in: SystemLogLoginIn) -> AbstractPage[SystemLogLoginOut]:
        """系统登录日志"""
        # 查询条件
        where = []
        if login_in.username:
            where.append(system_log_login.c.username.like(f'%{login_in.username}%'))
        if login_in.status:
            where.append(system_log_login.c.status == login_in.status)
        if login_in.start_time:
            where.append(system_log_login.c.create_time >= int(time.mktime(login_in.start_time.timetuple())))
        if login_in.end_time:
            where.append(system_log_login.c.create_time <= int(time.mktime(login_in.end_time.timetuple())))
        query = system_log_login.select().where(*where) \
            .order_by(system_log_login.c.id.desc())
        pager = await paginate(db, query)
        return pager

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
