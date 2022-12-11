import os

import aiofiles
from fastapi import UploadFile

from like.config import get_settings
from like.exceptions.base import AppException
from like.http_base import HttpResp

SIZE = 2048


class LocalStorage:

    @classmethod
    async def upload(cls, file_in: UploadFile, key: str, folder: str):
        directory = get_settings().upload_directory
        _date, save_name = key.split('/')
        save_path = os.path.join(directory, folder, _date).replace('\\', '/')
        file_name = os.path.join(save_path, save_name).replace('\\', '/')

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        try:
            async with aiofiles.open(file_name, 'wb') as file_out:
                content = await file_in.read(SIZE)
                while content:
                    await file_out.write(content)
                    content = await file_in.read(SIZE)
        except Exception as e:
            raise AppException(HttpResp.FAILED, msg='上传文件失败:%s' % e)
