import re
import time
from abc import ABC, abstractmethod

import pydantic
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select, or_

from like.admin.schemas.user import UserListIn, UserInfoOut, UserEditlIn, UserDetailIn
from like.common.enums import get_login_client, get_sex, SexEnum
from like.dependencies.database import db
from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.models import user_table
from like.utils.urls import UrlUtil


class IUserService(ABC):
    """用户信息抽象类"""

    @abstractmethod
    async def list(self, list_in: UserListIn) -> AbstractPage[UserInfoOut]:
        pass

    @abstractmethod
    async def edit(self, edit_in: UserEditlIn):
        pass

    @abstractmethod
    async def detail(self, detail_in: UserDetailIn) -> UserInfoOut:
        pass


class UserService(IUserService):
    """用户信息类"""
    select_columns = [user_table.c.id, user_table.c.nickname, user_table.c.channel, user_table.c.sn,
                      user_table.c.avatar, user_table.c.real_name, user_table.c.username, user_table.c.mobile,
                      user_table.c.sex, user_table.c.last_login_ip, user_table.c.last_login_time,
                      user_table.c.is_delete, user_table.c.create_time, user_table.c.update_time]

    async def list(self, list_in: UserListIn) -> AbstractPage[UserInfoOut]:
        where = [user_table.c.is_delete == 0]
        if list_in.keyword:
            where.append(or_(user_table.c.username.like('%{0}%'.format(list_in.keyword)),
                             user_table.c.nickname.like('%{0}%'.format(list_in.keyword)),
                             user_table.c.mobile.like('%{0}%'.format(list_in.keyword))))
        if list_in.channel:
            where.append(user_table.c.channel == list_in.channel)
        if list_in.start_time:
            where.append(user_table.c.create_time >= int(time.mktime(list_in.start_time.timetuple())))
        if list_in.end_time:
            where.append(user_table.c.create_time <= int(time.mktime(list_in.end_time.timetuple())))
        query = select(self.select_columns).select_from(user_table).where(*where).order_by(user_table.c.id.desc())

        user_list_pages = await paginate(db, query)
        for row in user_list_pages.lists:
            row.avatar = await UrlUtil.to_absolute_url(row.avatar)
            row.sex = get_sex(int(row.sex))
            row.channel = get_login_client(int(row.channel))
        return user_list_pages

    async def edit(self, edit_in: UserEditlIn):
        assert await db.fetch_one(
            select([user_table.c.id]).select_from(user_table).where(
                user_table.c.id == edit_in.id, user_table.c.is_delete == 0).limit(1)), '数据不存在！'

        if edit_in.field == 'username':
            assert len(edit_in.value) <= 32, '账号不能超过32个字符'
            assert not await db.fetch_one(
                select([user_table.c.id]).select_from(user_table).where(
                    user_table.c.username == edit_in.value, user_table.c.is_delete == 0).limit(1)), '当前账号已存在！'

        elif edit_in.field == 'realName':
            edit_in.field = 'real_name'
            assert len(edit_in.value) <= 32, '真实姓名不能超过32个字符'

        elif edit_in.field == 'mobile':
            assert re.match("^[1][3,4,5,6,7,8,9][0-9]{9}$", edit_in.value), '手机号格式不正确'
        elif edit_in.field == 'sex':
            if isinstance(edit_in.value, str):
                assert edit_in.value.isdigit(), '性别输入错误'
                edit_in.value = int(edit_in.value)
            assert edit_in.value in SexEnum.key_list(), '性别输入错误'
        else:
            raise AppException(HttpResp.FAILED, msg='不被支持的字段类型')

        edit_dict = {
            edit_in.field: edit_in.value,
            'update_time': int(time.time())
        }

        return await db.execute(user_table.update()
                                .where(user_table.c.id == edit_in.id)
                                .values(**edit_dict))

    async def detail(self, detail_in: UserDetailIn) -> UserInfoOut:
        user = await db.fetch_one(
            select(self.select_columns).select_from(user_table).where(
                user_table.c.id == detail_in.id, user_table.c.is_delete == 0).limit(1))

        assert user, '数据不存在！'

        result = pydantic.parse_obj_as(UserInfoOut, user)
        result.avatar = await UrlUtil.to_absolute_url(result.avatar)
        result.sex = get_sex(int(result.sex))
        result.channel = get_login_client(int(result.channel))
        return result

    @classmethod
    async def instance(cls, ):
        """实例化"""
        return cls()
