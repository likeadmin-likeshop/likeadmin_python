from fastapi import APIRouter

from like.http_base import unified_resp

router = APIRouter()


@router.get('/index')
@unified_resp
async def index():
    return
