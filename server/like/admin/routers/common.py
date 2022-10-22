from fastapi import APIRouter

from like.http_base import unified_resp

router = APIRouter(prefix='/common')


@router.get('/index/console')
@unified_resp
async def index_console():
    return
