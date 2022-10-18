import os

import aiofiles
from fastapi import APIRouter, UploadFile

from like.config import get_settings
from like.http_base import unified_resp

router = APIRouter(prefix='/upload')

SIZE = 2048


@router.post('/image')
@unified_resp
async def upload_image(file_in: UploadFile):
    async with aiofiles.open(f'{os.path.join(get_settings().upload_directory, file_in.filename)}', 'wb') as file_out:
        while content := await file_in.read(SIZE):
            await file_out.write(content)
    return {'filename': file_in.filename}
