from fastapi import APIRouter, Depends, Request

from like.front.service.user import IUserService, UserService
from like.http_base import unified_resp

router = APIRouter(prefix='/user')


@router.get('/center')
@unified_resp
async def center(request: Request, user_service: IUserService = Depends(UserService.instance)):
    """个人中心"""
    return await user_service.center(request.state.user_id)


@router.get('/info')
@unified_resp
async def info(request: Request, user_service: IUserService = Depends(UserService.instance)):
    """个人信息"""
    return await user_service.info(request.state.user_id)
