import time
from abc import ABC, abstractmethod

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate

from like.admin.schemas.channel import ChannelOaReplyDefaultCreateIn, ChannelOaReplyOut
from like.dependencies.database import db
from like.models import official_reply


class IChannelOaReplyDefaultService(ABC):
    """公众号默认回复服务抽象类"""

    @abstractmethod
    async def list(self) -> AbstractPage[ChannelOaReplyOut]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> ChannelOaReplyOut:
        pass

    @abstractmethod
    async def add(self, create_in: ChannelOaReplyDefaultCreateIn):
        pass


class ChannelOaReplyDefaultService(IChannelOaReplyDefaultService):
    """公众号默认回复服务实现类"""

    async def list(self) -> AbstractPage[ChannelOaReplyOut]:
        """默认回复列表"""
        query = official_reply.select() \
            .where(official_reply.c.reply_type == 3, official_reply.c.is_delete == 0) \
            .order_by(official_reply.c.sort.desc(), official_reply.c.id.desc())
        return await paginate(db, query)

    async def detail(self, id_: int) -> ChannelOaReplyOut:
        """默认回复详情"""
        reply = await db.fetch_one(
            official_reply.select()
            .where(official_reply.c.id == id_, official_reply.c.is_delete == 0)
            .limit(1))
        assert reply, '默认数据不存在!'
        return ChannelOaReplyOut.from_orm(reply)

    async def add(self, create_in: ChannelOaReplyDefaultCreateIn):
        """默认回复新增"""
        if create_in.status == 1:
            await db.execute(official_reply.update().where(official_reply.c.reply_type == 3).values({'status': 0}))
        create_dict = create_in.dict()
        create_dict['reply_type'] = 3
        create_dict['create_time'] = int(time.time())
        create_dict['update_time'] = int(time.time())
        await db.execute(official_reply.insert().values(**create_dict))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
