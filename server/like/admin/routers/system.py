import logging

from fastapi import APIRouter, Depends

from like.admin.schemas.system import SystemLoginIn
from like.admin.service.system.login import ISystemLoginService, SystemLoginService
from like.http_base import unified_resp

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/system')


@router.post('/login')
@unified_resp
async def login(login_in: SystemLoginIn, login_service: ISystemLoginService = Depends(SystemLoginService.instance)):
    return await login_service.login(login_in)


@router.get('/admin/self')
@unified_resp
async def admin_self():
    return


@router.get('/admin/list')
@unified_resp
async def admin_list():
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
