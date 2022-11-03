import time
from typing import Union

from like.dependencies.database import db
from like.models import system_config
from .tools import ToolsUtil

__all__ = ['ConfigUtil']


class ConfigUtil:
    """数据库配置操作工具"""

    @staticmethod
    async def get(type_: str, name: str = None) -> dict:
        """根据类型和名称获取配置字典"""
        where = [system_config.c.type == type_]
        if name:
            where.append(system_config.c.name == name)
        configs = await db.fetch_all(system_config.select().where(*where))
        return {i.name: i.value for i in configs}

    @staticmethod
    async def get_val(type_: str, name: str, default: str = None) -> Union[str, None]:
        """根据类型和名称获取配置值"""
        config = await ConfigUtil.get(type_, name)
        if name not in config:
            return default
        return config.get(name)

    @staticmethod
    async def get_map(type_: str, name: str) -> Union[dict, None]:
        """根据类型和名称获取配置值(Json字符串转dict)"""
        value = await ConfigUtil.get_val(type_, name)
        if value is None:
            return None
        if not value:
            return {}
        return ToolsUtil.json_to_map(value)

    @staticmethod
    async def set(type_: str, name: str, val: str):
        """设置配置的值"""
        config = await db.fetch_one(
            system_config.select().where(
                system_config.c.type == type_, system_config.c.name == name).limit(1))
        if config:
            await db.execute(
                system_config.update().where(
                    system_config.c.id == config.id).values(value=val, update_time=int(time.time())))
        else:
            await db.execute(
                system_config.insert().values(
                    type=type_, name=name, value=val, create_time=int(time.time()), update_time=int(time.time())))
