import time
from abc import ABC, abstractmethod
from typing import List

import pydantic
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select

from like.admin.schemas.common import CommonAlbumListIn, CommonAlbumCateListIn, CommonAlbumCateOut, \
    CommonAlbumCateEditIn, CommonAlbumAddIn, CommonAlbumCateDelIn, CommonAlbumRenameIn, CommonAlbumMoveIn, \
    CommonAlbumDelIn, CommonAlbumOut
from like.dependencies.database import db
from like.models.common import common_album, common_album_cate
from like.utils.array import ArrayUtil
from like.utils.urls import UrlUtil


class IAlbumService(ABC):
    """相册服务抽象类"""

    @abstractmethod
    async def album_list(self, params: CommonAlbumListIn) -> AbstractPage[CommonAlbumOut]:
        """
        文件列表
        :param params:
        :return:
        """
        pass

    @abstractmethod
    async def album_rename(self, params: CommonAlbumRenameIn):
        """
        文件重命名
        :param params:
        :return:
        """
        pass

    @abstractmethod
    async def album_move(self, params: CommonAlbumMoveIn):
        """
        文件移动
        :param params:
        :return:
        """
        pass

    @abstractmethod
    async def album_add(self, params: CommonAlbumAddIn):
        """
        文件新增
        :param params:
        :return:
        """
        pass

    @abstractmethod
    async def album_del(self, params: CommonAlbumDelIn):
        """
        文件删除
        :param params:
        :return:
        """

    @abstractmethod
    async def cate_list(self, params: CommonAlbumCateListIn):
        """
        分类列表
        :param params:
        :return:
        """

    @abstractmethod
    async def cate_add(self, params: CommonAlbumCateEditIn):
        """
        分类新增
        :param params:
        :return:
        """

    @abstractmethod
    async def cate_rename(self, params: CommonAlbumRenameIn):
        """
        分类重命名
        :param params:
        :return:
        """

    @abstractmethod
    async def cate_del(self, params: CommonAlbumCateDelIn):
        """
        分类删除
        :param params:
        :return:
        """


class AlbumService(IAlbumService):
    """主页服务实现类"""
    select_album_columns = [common_album.c.id, common_album.c.cid, common_album.c.name, common_album.c.ext,
                            common_album.c.uri, common_album.c.size, common_album.c.create_time,
                            common_album.c.update_time]
    select_album_cate_columns = [common_album_cate.c.id, common_album_cate.c.name, common_album_cate.c.type,
                                 common_album_cate.c.pid, common_album_cate.c.create_time,
                                 common_album_cate.c.update_time]
    album_order_by = [common_album.c.id.desc()]
    cate_order_by = [common_album_cate.c.id.desc()]

    async def album_list(self, params: CommonAlbumListIn) -> AbstractPage[CommonAlbumOut]:
        where = [common_album.c.is_delete == 0]
        if params.cid is not None:
            where.append(common_album.c.cid == params.cid)
        if params.type:
            where.append(common_album.c.type == params.type)
        if params.keyword:
            where.append(common_album.c.name.like('%{0}%'.format(params.keyword)))
        query = select(self.select_album_columns).select_from(common_album).where(*where).order_by(*self.album_order_by)

        pager = await paginate(db, query)
        for row in pager.lists:
            row.url = await UrlUtil.to_absolute_url(row.url)
        return pager

    async def album_rename(self, params: CommonAlbumRenameIn):
        _id = params.id
        album = await db.fetch_one(
            select([common_album.c.id, common_album.c.name]).select_from(common_album).where(common_album.c.id == _id,
                                                                                             common_album.c.is_delete == 0))
        assert album, "文件丢失！"
        album_dict = {
            'name': params.name,
            'update_time': int(time.time())
        }
        return await db.execute(common_album.update()
                                .where(common_album.c.id == _id)
                                .values(**album_dict))

    async def album_move(self, params: CommonAlbumMoveIn):
        """
        文件移动
        :param params:
        :return:
        """
        cid = params.cid
        ids = params.ids
        albums = await db.fetch_all(
            select([common_album.c.id, common_album.c.name]).select_from(common_album).where(common_album.c.id.in_(ids),
                                                                                             common_album.c.is_delete == 0))
        assert albums, "文件丢失！"

        if cid > 0:
            assert await db.fetch_one(
                select([common_album_cate.c.id, common_album_cate.c.name, ]).select_from(common_album_cate).where(
                    common_album_cate.c.id == cid, common_album_cate.c.is_delete == 0)), '分类已不存在'
        return await db.execute_many(common_album.update().where(common_album.c.id.in_(ids)),
                                     [{'cid': cid, 'update_time': int(time.time())}])

    async def album_add(self, params: CommonAlbumAddIn):
        """
        文件新增
        :param params:
        :return:
        """
        create_dict = {
            'cid': params.cid,
            'aid': params.aid,
            'uid': params.uid,
            'name': params.name,
            'ext': params.ext,
            'uri': params.url,
            'size': params.size,
            'type': params.type,
            'create_time': int(time.time()),
            'update_time': int(time.time())
        }
        query = common_album.insert().values(**create_dict)
        return await db.execute(query)

    async def album_del(self, params: CommonAlbumDelIn):
        """
        文件删除
        :param params:
        :return:
        """
        ids = params.ids
        albums = await db.fetch_all(
            select([common_album.c.id, common_album.c.name]).select_from(common_album).where(common_album.c.id.in_(ids),
                                                                                             common_album.c.is_delete == 0))
        assert albums, "文件丢失！"
        return await db.execute_many(common_album.update()
                                     .where(common_album.c.id.in_(ids)),
                                     [{'is_delete': 1, 'delete_time': int(time.time())}])

    async def cate_list(self, params: CommonAlbumCateListIn):
        """
        分类列表
        :param params:
        :return:
        """
        _type = params.type
        keyword = params.keyword
        where = [common_album_cate.c.is_delete == 0]
        if _type:
            where.append(common_album_cate.c.type == _type)
        if keyword:
            where.append(common_album_cate.c.name.like('%{0}%'.format(keyword)))

        cate_list = await db.fetch_all(
            select(self.select_album_cate_columns).select_from(common_album_cate).where(*where).order_by(
                *self.cate_order_by))
        return ArrayUtil.list_to_tree(
            [i.dict(exclude_none=True) for i in pydantic.parse_obj_as(List[CommonAlbumCateOut], cate_list)],
            'id', 'pid', 'children')

    async def cate_add(self, params: CommonAlbumCateEditIn):

        if params.pid and params.pid > 0:
            assert await db.fetch_one(
                select([common_album_cate.c.id, common_album_cate.c.name, ]).select_from(common_album_cate).where(
                    common_album_cate.c.id == params.pid, common_album_cate.c.is_delete == 0)), '父级分类不存在'

        create_dict = {
            'type': params.type,
            'pid': params.pid,
            'name': params.name,
            'create_time': int(time.time()),
            'update_time': int(time.time())
        }
        query = common_album_cate.insert().values(**create_dict)
        return await db.execute(query)

    async def cate_rename(self, params: CommonAlbumRenameIn):
        _id = params.id
        name = params.name
        assert await db.fetch_one(
            select([common_album_cate.c.id, common_album_cate.c.name, ]).select_from(common_album_cate).where(
                common_album_cate.c.id == _id, common_album_cate.c.is_delete == 0)), '分类已不存在'
        edit_cate = {
            'name': name,
            'update_time': int(time.time())
        }
        return await db.execute(common_album_cate.update()
                                .where(common_album_cate.c.id == _id)
                                .values(**edit_cate))

    async def cate_del(self, params: CommonAlbumCateDelIn):
        _id = params.id
        assert await db.fetch_one(
            select([common_album_cate.c.id, common_album_cate.c.name]).select_from(common_album_cate).where(
                common_album_cate.c.id == _id, common_album_cate.c.is_delete == 0)), '分类已不存在'

        assert not await db.fetch_one(
            select([common_album_cate.c.id, common_album_cate.c.name]).select_from(common_album_cate).where(
                common_album_cate.c.pid == _id, common_album_cate.c.is_delete == 0)), '当前分类正被使用中,不能删除！'

        assert not await db.fetch_one(
            select([common_album.c.id, common_album.c.name]).select_from(common_album).where(
                common_album.c.cid == params.id,
                common_album.c.is_delete == 0)), '当前分类正被使用中,不能删除！'

        return await db.execute(common_album_cate.update()
                                .where(common_album_cate.c.id == _id)
                                .values(is_delete=1, delete_time=int(time.time())))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
