from fastapi import APIRouter, Depends

from like.front.schemas.index import PolicyIn
from like.front.service.index import IndexService, IIndexService
from like.http_base import unified_resp

router = APIRouter()


@router.get('/index')
@unified_resp
async def index(index_service: IIndexService = Depends(IndexService.instance)):
    return await index_service.index()


@router.get("/policy")
async def policy(policy_in: PolicyIn = Depends(), index_service: IIndexService = Depends(IndexService.instance)):
    return await index_service.policy(policy_in)
