from fastapi import APIRouter, Depends

from like.front.schemas.article import ArticleSearchOut
from like.front.schemas.index import PolicyIn, SearchIn
from like.front.service.index import IIndexService, IndexService
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter()


@router.get('/index')
@unified_resp
async def index():
    return


@router.get('/policy')
@unified_resp
async def policy(policy_in: PolicyIn = Depends(), index_service: IIndexService = Depends(IndexService.instance)):
    """协议"""
    return await index_service.policy(policy_in.type)


@router.get('/hotSearch')
@unified_resp
async def hot_search(index_service: IIndexService = Depends(IndexService.instance)):
    """热搜"""
    return await index_service.hot_search()


@router.get('/search', response_model=PageInationResult[ArticleSearchOut])
@unified_resp
async def search(search_in: SearchIn = Depends(), index_service: IIndexService = Depends(IndexService.instance)):
    """搜索"""
    return await index_service.search(search_in)
