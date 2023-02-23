from fastapi import APIRouter, Depends

from like.http_base import unified_resp
from like.front.service.index import IndexService, IIndexService
router = APIRouter()


@router.get('/index')
@unified_resp
async def index(index_service: IIndexService = Depends(IndexService.instance)):
    return await index_service.index()
