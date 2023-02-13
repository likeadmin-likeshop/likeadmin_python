from fastapi import APIRouter, Depends

from like.admin.schemas.user import UserListIn, UserDetailIn, UserEditlIn
from like.admin.service.user.user import IUserService, UserService, UserInfoOut
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter(prefix='/user')


@router.get('/list', response_model=PageInationResult[UserInfoOut])
@unified_resp
async def user_list(list_in: UserListIn = Depends(),
                    user_service: IUserService = Depends(UserService.instance)):
    """
    用户列表
    :return:
    """
    return await user_service.list(list_in)


@router.get('/detail')
@unified_resp
async def user_detail(detail_in: UserDetailIn = Depends(),
                      user_service: IUserService = Depends(UserService.instance)) -> UserInfoOut:
    """
    用户详情
    :return:
    """
    return await user_service.detail(detail_in=detail_in)

@router.post('/edit')
@unified_resp
async def user_detail(edit_in: UserEditlIn,
                      user_service: IUserService = Depends(UserService.instance)) -> UserInfoOut:
    """
    用户修改
    :return:
    """
    return await user_service.edit(edit_in=edit_in)

