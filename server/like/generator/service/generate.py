from abc import ABC, abstractmethod
from typing import List

from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select, text, and_

from like.dependencies.database import db
from like.generator.schemas.generate import (DbTablesIn, EditTableIn, DbTableOut, GenTableOut)


class IGenerateService(ABC):
    """代码生成服务抽象类"""

    @abstractmethod
    async def db_tables(self, db_in: DbTablesIn) -> AbstractPage[DbTableOut]:
        pass

    @abstractmethod
    async def list(self) -> AbstractPage[GenTableOut]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> dict:
        pass

    @abstractmethod
    async def import_table(self, table_names: List[str]):
        pass

    @abstractmethod
    async def edit_table(self, edit_in: EditTableIn):
        pass

    @abstractmethod
    async def delete_table(self, ids: List[int]):
        pass

    @abstractmethod
    async def sync_table(self, id_: int):
        pass

    @abstractmethod
    async def preview_table(self, id_: int):
        pass

    @abstractmethod
    async def gen_table(self, table_name: str):
        pass

    @abstractmethod
    async def download_table(self, table_names: List[str]):
        pass


class GenerateService(IGenerateService):
    """代码生成服务实现类"""

    async def db_tables(self, db_in: DbTablesIn) -> AbstractPage[DbTableOut]:
        """库表列表"""
        where = []
        if db_in.table_name:
            where.append(text(f'lower(table_name) like lower("%{db_in.table_name}%")'))
        if db_in.table_comment:
            where.append(text(f'lower(table_comment) like lower("%{db_in.table_comment}%")'))
        query_str = (
            select(text('table_name, table_comment, create_time, update_time'))
            .where(
                and_(
                    text('table_schema = (SELECT database())'),
                    text('table_name NOT LIKE "qrtz_%"'),
                    text('table_name NOT LIKE "gen_%"'),
                    text('table_name NOT IN (select table_name from la_gen_table)'),
                    *where
                )
            )
            .select_from(text('information_schema.tables'))
        )
        pager = await paginate(db, query_str)
        return pager

    async def list(self) -> AbstractPage[GenTableOut]:
        pass

    async def detail(self, id_: int) -> dict:
        pass

    async def import_table(self, table_names: List[str]):
        pass

    async def edit_table(self, edit_in: EditTableIn):
        pass

    async def delete_table(self, ids: List[int]):
        pass

    async def sync_table(self, id_: int):
        pass

    async def preview_table(self, id_: int):
        pass

    async def gen_table(self, table_name: str):
        pass

    async def download_table(self, table_names: List[str]):
        pass

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
