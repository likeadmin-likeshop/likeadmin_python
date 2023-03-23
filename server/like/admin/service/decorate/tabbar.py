import json
import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from sqlalchemy import select

from like.admin.schemas.decorate import DecorateTabbarOut, DecorateTabbarStyle, DecorateTabbarList, \
    DecorateTabbarSaveIn
from like.dependencies.database import db
from like.models.decorate import decorate_tabbar
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IDecorateTabbarService(ABC):
    @abstractmethod
    async def detail(self) -> DecorateTabbarOut:
        pass

    @abstractmethod
    async def save(self, save_in: DecorateTabbarSaveIn):
        pass


class DecorateTabbarService(ABC):
    select_columns = [decorate_tabbar.c.id, decorate_tabbar.c.name, decorate_tabbar.c.selected,
                      decorate_tabbar.c.unselected, decorate_tabbar.c.link, decorate_tabbar.c.create_time,
                      decorate_tabbar.c.update_time]

    async def detail(self) -> DecorateTabbarOut:
        tabbar_list = await db.fetch_all(
            select(self.select_columns).select_from(decorate_tabbar).order_by(decorate_tabbar.c.id.asc()))
        tabbar_style = await ConfigUtil.get_val("tabbar", "style", "{}")

        style = pydantic.parse_obj_as(DecorateTabbarStyle, json.loads(tabbar_style))
        tabbar_list = pydantic.parse_obj_as(List[DecorateTabbarList], tabbar_list)

        return pydantic.parse_obj_as(DecorateTabbarOut, {"style": style, "list": tabbar_list})

    @db.transaction()
    async def save(self, save_in: DecorateTabbarSaveIn):
        await db.execute(decorate_tabbar.delete().where(decorate_tabbar.c.id > 0))

        tabbar_list = save_in.list

        for obj in tabbar_list:
            save_dict = {
                "name": obj.name,
                "selected": await UrlUtil.to_relative_url(obj.selected),
                "unselected": await UrlUtil.to_relative_url(obj.unselected),
                "link": obj.link,
                "update_time": int(time.time()),
                "create_time": int(time.time())
            }
            await db.execute(decorate_tabbar.insert().values(**save_dict))
        tabbar_style = save_in.style
        if tabbar_style:
            await ConfigUtil.set("tabbar", "style", json.dumps(tabbar_style.dict()))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
