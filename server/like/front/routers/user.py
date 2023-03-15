from fastapi import APIRouter, Depends, Request

from like.front.schemas.user import UserEditIn, UserChangePwdIn, UserBindMobileIn
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


@router.post('/edit')
@unified_resp
async def edit(request: Request, edit_in: UserEditIn, user_service: IUserService = Depends(UserService.instance)):
    """编辑信息"""
    return await user_service.edit(request.state.user_id, edit_in)


@router.post('/changePwd')
@unified_resp
async def change_pwd(request: Request, change_in: UserChangePwdIn,
                     user_service: IUserService = Depends(UserService.instance)):
    """修改密码"""
    return await user_service.change_pwd(request.state.user_id, change_in)


@router.post('/bindMobile')
@unified_resp
async def bind_mobile(request: Request, bind_in: UserBindMobileIn,
                      user_service: IUserService = Depends(UserService.instance)):
    """绑定手机号"""
    return await user_service.bind_mobile(request.state.user_id, bind_in)
