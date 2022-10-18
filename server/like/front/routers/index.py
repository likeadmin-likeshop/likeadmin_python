from fastapi import APIRouter
from fastapi_cache.decorator import cache

from like.http_base import unified_resp

router = APIRouter()


@router.get('/index')
@unified_resp
async def index():
    return


@cache(expire=10)
async def get_cache():
    import random
    return random.randint(1, 10)


@router.get('/test/redis')
@unified_resp
async def test_redis():
    return {'get_cache': await get_cache()}
