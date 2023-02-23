from fastapi import APIRouter, Depends

from like.common.enums import LoginTypeEnum
from like.front.schemas.login import FrontLoginCheckIn, FrontRegisterIn
from like.front.service.login import ILoginService, LoginService
from like.http_base import unified_resp

router = APIRouter(prefix='/login')


@router.post('/check')
@unified_resp
async def login_check(
        params: FrontLoginCheckIn,
        login_service: ILoginService = Depends(LoginService.instance)
):
    """
    登录管理
    :return:
    """
    scene = params.scene
    if scene == LoginTypeEnum.account:
        return await login_service.account_login(params.username, params.password)
    elif scene == LoginTypeEnum.mobile:
        return await login_service.mobile_login(params.mobile, params.code)
    elif scene == LoginTypeEnum.mnp:
        return await login_service.mnp_login(params.code, params.client)
    elif scene == LoginTypeEnum.office:
        return await login_service.office_login(params.code, params.client)


@router.post('/register')
@unified_resp
async def register(params: FrontRegisterIn, login_service: ILoginService = Depends(LoginService.instance)):
    """
    注册
    :return:
    """
    return await login_service.register(params)
