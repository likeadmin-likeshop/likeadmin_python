from fastapi import APIRouter, Depends

from like.http_base import unified_resp
from like.admin.service.common.index import IIndexService, IndexService

router = APIRouter(prefix='/common')


@router.get('/index/console')
@unified_resp
async def index_console(index_service: IIndexService = Depends(IndexService.instance)):
    """控制台"""
    return await index_service.console()


@router.get('/index/config')
@unified_resp
async def index_config(index_service: IIndexService = Depends(IndexService.instance)):
    """公共配置"""
    return await index_service.config()
