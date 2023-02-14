import time
from abc import ABC, abstractmethod

import pydantic
from sqlalchemy import select

from like.admin.schemas.decorate import DecoratePageSaveIn, DecoratePageDetailOut
from like.dependencies.database import db
from like.models.decorate import decorate_page


class IDecoratePageService(ABC):
    @abstractmethod
    async def detail(self, _id: int) -> DecoratePageDetailOut:
        pass

    @abstractmethod
    async def save(self, save_in: DecoratePageSaveIn):
        pass


class DecoratePageService(ABC):
    select_columns = [decorate_page.c.id, decorate_page.c.page_type, decorate_page.c.page_data]

    async def detail(self, _id: int) -> DecoratePageDetailOut:
        page_detail = await db.fetch_one(
            select(self.select_columns).select_from(decorate_page).where(
                decorate_page.c.id == _id).limit(1))
        assert page_detail, '数据不存在！'
        return pydantic.parse_obj_as(DecoratePageDetailOut, page_detail)

    async def save(self, save_in: DecoratePageSaveIn):
        page_detail = await db.fetch_one(
            select(self.select_columns).select_from(decorate_page).where(
                decorate_page.c.id == save_in.id).limit(1))
        assert page_detail, '数据不存在！'
        page_edit = save_in.dict()
        page_edit['update_time'] = int(time.time())
        return await db.execute(decorate_page.update()
                                .where(decorate_page.c.id == save_in.id)
                                .values(**page_edit))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
