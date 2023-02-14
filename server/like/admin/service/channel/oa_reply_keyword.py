import time
from abc import ABC, abstractmethod

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate

from like.admin.schemas.channel import ChannelOaReplyKeywordCreateIn, ChannelOaReplyKeywordEditIn, ChannelOaReplyOut
from like.dependencies.database import db
from like.models import official_reply


class IChannelOaReplyKeywordService(ABC):
    """公众号关键词回复服务抽象类"""

    @abstractmethod
    async def list(self) -> AbstractPage[ChannelOaReplyOut]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> ChannelOaReplyOut:
        pass

    @abstractmethod
    async def add(self, create_in: ChannelOaReplyKeywordCreateIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: ChannelOaReplyKeywordEditIn):
        pass

    @abstractmethod
    async def delete(self, id_: int):
        pass

    @abstractmethod
    async def status(self, id_: int):
        pass


class ChannelOaReplyKeywordService(IChannelOaReplyKeywordService):
    """公众号关键词回复服务实现类"""

    async def list(self) -> AbstractPage[ChannelOaReplyOut]:
        """关键词回复列表"""
        query = official_reply.select() \
            .where(official_reply.c.reply_type == 2, official_reply.c.is_delete == 0) \
            .order_by(official_reply.c.sort.desc(), official_reply.c.id.desc())
        return await paginate(db, query)

    async def detail(self, id_: int) -> ChannelOaReplyOut:
        """关键词回复详情"""
        reply = await db.fetch_one(
            official_reply.select()
            .where(official_reply.c.id == id_, official_reply.c.reply_type == 2, official_reply.c.is_delete == 0)
            .limit(1))
        assert reply, '关键词回复数据不存在!'
        return ChannelOaReplyOut.from_orm(reply)

    async def add(self, create_in: ChannelOaReplyKeywordCreateIn):
        """关键词回复新增"""
        create_dict = create_in.dict()
        create_dict['reply_type'] = 2
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(official_reply.insert().values(**create_dict))

    @db.transaction()
    async def edit(self, edit_in: ChannelOaReplyKeywordEditIn):
        """关键词回复编辑"""
        reply = await db.fetch_one(
            official_reply.select()
            .where(official_reply.c.id == edit_in.id, official_reply.c.reply_type == 2, official_reply.c.is_delete == 0)
            .limit(1))
        assert reply, '关键词回复数据不存在!'
        edit_dict = edit_in.dict()
        edit_dict['reply_type'] = 2
        edit_dict['update_time'] = int(time.time())
        await db.execute(official_reply.update().where(official_reply.c.id == edit_in.id).values(**edit_dict))

    async def delete(self, id_: int):
        """关键词回复删除"""
        reply = await db.fetch_one(
            official_reply.select()
            .where(official_reply.c.id == id_, official_reply.c.reply_type == 2, official_reply.c.is_delete == 0)
            .limit(1))
        assert reply, '关键词回复数据不存在!'
        await db.execute(official_reply.update().where(official_reply.c.id == id_).values(
            {'is_delete': 1, 'delete_time': int(time.time())}))

    async def status(self, id_: int):
        """关键词回复状态"""
        reply = await db.fetch_one(
            official_reply.select()
            .where(official_reply.c.id == id_, official_reply.c.reply_type == 2, official_reply.c.is_delete == 0)
            .limit(1))
        assert reply, '关键词回复数据不存在!'
        status = 0 if reply.status else 1
        await db.execute(official_reply.update().where(official_reply.c.id == id_).values(
            {'status': status, 'update_time': int(time.time())}))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
