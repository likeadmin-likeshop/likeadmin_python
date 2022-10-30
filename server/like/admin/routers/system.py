import logging
from typing import Union

from fastapi import APIRouter, Depends, Request, Header
from fastapi.params import Query

from like.admin.schemas.page import PageInationResult
from like.admin.schemas.system import (
    SystemLoginIn, SystemLogoutIn, SystemAuthAdminListIn, SystemAuthAdminDetailIn, SystemAuthAdminCreateIn,
    SystemAuthAdminDelIn, SystemAuthAdminDisableIn, SystemAuthAdminEditIn, SystemAuthAdminUpdateIn,
    SystemAuthAdminOut, SystemAuthPostOut)
from like.admin.service.system.auth_admin import ISystemAuthAdminService, SystemAuthAdminService
from like.admin.service.system.auth_role import ISystemAuthRoleService, SystemAuthRoleService
from like.admin.service.system.auth_post import ISystemAuthPostService, SystemAuthPostService
from like.admin.service.system.login import ISystemLoginService, SystemLoginService
from like.http_base import unified_resp

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/system')


@router.post('/login')
@unified_resp
async def login(login_in: SystemLoginIn, login_service: ISystemLoginService = Depends(SystemLoginService.instance)):
    """登录系统"""
    return await login_service.login(login_in)


@router.post('/logout')
@unified_resp
async def logout(token: str = Header(),
                 login_service: ISystemLoginService = Depends(SystemLoginService.instance)):
    """退出登录"""
    return await login_service.logout(SystemLogoutIn(token=token))


@router.get('/admin/self')
@unified_resp
async def admin_self(request: Request,
                     auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员信息"""
    return await auth_service.self(request.state.admin_id)


@router.get('/admin/list', response_model=PageInationResult[SystemAuthAdminOut])
@unified_resp
async def admin_list(list_in: SystemAuthAdminListIn = Depends(),
                     auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员列表"""
    return await auth_service.list(list_in)


@router.get('/admin/detail')
@unified_resp
async def admin_detail(detail_in: SystemAuthAdminDetailIn = Depends(),
                       auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员详细"""
    return await auth_service.detail(detail_in.id)


@router.post('/admin/add')
@unified_resp
async def admin_add(admin_create_in: SystemAuthAdminCreateIn,
                    auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员新增"""
    return await auth_service.add(admin_create_in)


@router.post('/admin/edit')
@unified_resp
async def admin_edit(admin_edit_in: SystemAuthAdminEditIn,
                     auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员编辑"""
    return await auth_service.edit(admin_edit_in)


@router.post('/admin/upInfo')
@unified_resp
async def admin_upinfo(request: Request, admin_update_in: SystemAuthAdminUpdateIn,
                       auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员更新"""
    return await auth_service.update(admin_update_in, request.state.admin_id)


@router.post('/admin/del')
@unified_resp
async def admin_del(admin_del_in: SystemAuthAdminDelIn,
                    auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员删除"""
    return await auth_service.delete(admin_del_in.id)


@router.post('/admin/disable')
@unified_resp
async def admin_disable(admin_disable_in: SystemAuthAdminDisableIn,
                        auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员状态切换"""
    return await auth_service.disable(admin_disable_in.id)


@router.get('/menu/route')
@unified_resp
async def menu_route():
    return


@router.get('/menu/list')
@unified_resp
async def menu_list():
    return


@router.get('/role/all')
@unified_resp
async def role_all(role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
    """角色所有"""
    return await role_service.all()


@router.get('/role/list')
@unified_resp
async def role_list():
    return


@router.get('/role/detail')
@unified_resp
async def role_detail():
    return


@router.post('/role/add')
@unified_resp
async def role_add():
    return


@router.post('/role/edit')
@unified_resp
async def role_edit():
    return


@router.post('/role/del')
@unified_resp
async def role_del():
    return


# 岗位相关接口
@router.get('/post/all')
async def post_all(post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.fetch_all()


@router.get('/post/detail')
@unified_resp
async def post_detail():
    return {}


@router.get('/post/list', response_model=PageInationResult[SystemAuthPostOut])
@unified_resp
async def post_list(code: Union[str, None] = Query(default=None), status: Union[int, None] = Query(default=None),
                    name: Union[str, None] = Query(default=None),
                    post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.fetch_list(code=code, name=name, is_stop=status)


@router.post('/post/add')
@unified_resp
async def post_add():
    return {}


@router.post('/post/delete')
@unified_resp
async def post_delete():
    return {}


@router.post('/post/edit')
@unified_resp
async def post_edit():
    return {}
