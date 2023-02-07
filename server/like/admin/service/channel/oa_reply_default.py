from abc import ABC, abstractmethod

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate

from like.dependencies.database import db
from like.models import official_reply
from like.admin.schemas.channel import ChannelOaReplyOut


class IChannelOaReplyDefaultService(ABC):
    """公众号默认回复服务抽象类"""

    @abstractmethod
    async def list(self) -> AbstractPage[ChannelOaReplyOut]:
        pass


class ChannelOaReplyDefaultService(IChannelOaReplyDefaultService):
    """公众号默认回复服务实现类"""

    async def list(self) -> AbstractPage[ChannelOaReplyOut]:
        """默认回复列表"""
        query = official_reply.select() \
            .where(official_reply.c.reply_type == 3, official_reply.c.is_delete == 0) \
            .order_by(official_reply.c.sort.desc(), official_reply.c.id.desc())
        return await paginate(db, query)

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
