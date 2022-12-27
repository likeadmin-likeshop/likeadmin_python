import os.path

from fastapi import UploadFile

from like.config import get_settings
from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.plugins.storage.engine.aliyun import AliyunStorage
from like.plugins.storage.engine.local import LocalStorage
from like.plugins.storage.engine.qiniu import QiniuStorage
from like.plugins.storage.engine.qcloud import QCloudStorage
from like.utils.config import ConfigUtil
from like.utils.datetime import get_now_str, FORMAT_DATE2
from like.utils.tools import ToolsUtil
from like.utils.urls import UrlUtil


class StorageDriver(object):

    @classmethod
    async def upload(cls, file_in: UploadFile, folder: str, file_type: int):
        engine = await ConfigUtil.get_val("storage", "default", "local")
        file_size = cls.get_file_size(file_in)
        cls.check_file(file_in, file_size, file_type)
        key = cls.build_save_name(file_in, folder)
        if engine == 'local':
            await LocalStorage.upload(file_in, key)
            key = key.replace('\\', '/')
        elif engine == 'qiniu':
            result = await QiniuStorage().upload_data(key, file_in.file)
            key = result['key']
        elif engine == 'aliyun':
            key = await AliyunStorage().upload_data(key, file_in.file)
        elif engine == 'qcloud':
            key = await QCloudStorage().upload_data(key, file_in.file)
        else:
            raise AppException(HttpResp.FAILED, msg="engine:%s 暂未接入, 暂时不支持" % engine)

        origin_file_name = file_in.filename
        origin_ext = origin_file_name.split('.')[-1].lower()

        result = {
            'name': origin_file_name,
            'size': file_size,
            'ext': origin_ext,
            'url': key,
            'path': await UrlUtil.to_absolute_url(key)
        }
        return result

    @classmethod
    def build_save_name(cls, file_in: UploadFile, folder):
        """
        保存的文件名
        :return:
        """
        date = get_now_str(FORMAT_DATE2)
        filename = file_in.filename
        ext = filename.split('.')[-1].lower()
        uuid = ToolsUtil.make_uuid()
        return folder + "/" + date + "/" + uuid + '.' + ext

    @classmethod
    def check_file(cls, file_in: UploadFile, file_size: int, file_type: int):
        filename = file_in.filename
        ext = filename.split('.')[-1].lower()
        if not ext:
            raise AppException(HttpResp.FAILED, msg='未知的文件类型')
        if file_type == 10:
            # 图片文件
            limit_size = get_settings().upload_image_size
            if ext not in get_settings().upload_image_ext:
                raise AppException(HttpResp.FAILED, msg='不被支持的扩展:%s' % ext)
            if file_size > limit_size:
                raise AppException(HttpResp.FAILED, msg='上传图片不能超出限制:%d M' % (limit_size / 1024 / 1024))
        elif file_type == 20:
            # 视频文件
            limit_size = get_settings().upload_video_size
            if ext not in get_settings().upload_video_ext:
                raise AppException(HttpResp.FAILED, msg='不被支持的扩展:%s' % ext)
            if file_size > limit_size:
                raise AppException(HttpResp.FAILED, msg='上传图片不能超出限制:%d M' % (limit_size / 1024 / 1024))
        else:
            raise AppException(HttpResp.FAILED, msg='上传文件类型错误')

    @classmethod
    def get_file_size(cls, file_in: UploadFile):
        file_in.file.seek(0, os.SEEK_END)
        file_size = file_in.file.tell()
        file_in.file.seek(0, os.SEEK_SET)
        return file_size
