import logging

from fastapi import APIRouter, Depends, Header

from like.admin.schemas.system import SystemLoginIn, SystemLogoutIn
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
    await login_service.logout(SystemLogoutIn(token=token))
    return


@router.get('/admin/self')
@unified_resp
async def admin_self():
    return


@router.get('/admin/list')
@unified_resp
async def admin_list():
    return


@router.get('/admin/detail')
@unified_resp
async def admin_detail():
    return


@router.post('/admin/add')
@unified_resp
async def admin_add():
    return


@router.post('/admin/edit')
@unified_resp
async def admin_edit():
    return


@router.post('/admin/upInfo')
@unified_resp
async def admin_upinfo():
    return


@router.post('/admin/del')
@unified_resp
async def admin_del():
    return


@router.post('/admin/disable')
@unified_resp
async def admin_disable():
    return


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
async def role_all():
    return


@router.get('/role/list')
@unified_resp
async def role_list():
    return
