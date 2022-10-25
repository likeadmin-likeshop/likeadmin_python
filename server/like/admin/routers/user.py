from fastapi import APIRouter

from like.http_base import unified_resp

router = APIRouter(prefix='/user')


@router.get('/list')
@unified_resp
async def user_list():
    return