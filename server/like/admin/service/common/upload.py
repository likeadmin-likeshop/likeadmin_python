from abc import ABC, abstractmethod

from fastapi import UploadFile, Depends, Request

from like.admin.schemas.common import CommonAlbumAddIn
from like.admin.service.common.album import IAlbumService, AlbumService
from like.plugins.storage.storage_driver import StorageDriver


class IUploadService(ABC):
    """上传文件服务类"""

    @abstractmethod
    async def upload_image(self, file_in: UploadFile, cid: int):
        """
        上传图片
        :param file_in:
        :param cid:
        :return:
        """

    async def upload_video(self, file_in: UploadFile, cid: int):
        """
        上传视频
        :param file_in:
        :param cid:
        :return:
        """


class UploadService(IUploadService):

    async def upload_image(self, file_in: UploadFile, cid: int):
        result = await StorageDriver.upload(file_in, 'image', 10)
        album_add_params = CommonAlbumAddIn(**{
            'aid': self.request.state.admin_id,
            'cid': cid,
            'uid': 0,
            'type': 10,
            'size': result['size'],
            'ext': result['ext'],
            'url': result['url'],
            'name': result['name']
        })
        album_id = await self.album_service.album_add(album_add_params)
        result.update({'id': album_id})
        return result

    async def upload_video(self, file_in: UploadFile, cid: int):
        result = await StorageDriver.upload(file_in, 'video', 20)

        album_add_params = CommonAlbumAddIn(**{
            'aid': self.request.state.admin_id,
            'cid': cid,
            'uid': 0,
            'type': 20,
            'size': result['size'],
            'ext': result['ext'],
            'url': result['url'],
            'name': result['name']
        })
        album_id = await self.album_service.album_add(album_add_params)
        result.update({'id': album_id})
        return result

    def __init__(self, request, album_service: IAlbumService):
        self.album_service: IAlbumService = album_service
        self.request: Request = request

    @classmethod
    async def instance(cls, request: Request, album_service: IAlbumService = Depends(AlbumService.instance)):
        """实例化"""
        return cls(request, album_service)
