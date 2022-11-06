import logging
from typing import Union

from fastapi import APIRouter, Depends, Request, Header
from fastapi.params import Query

from like.admin.schemas.page import PageInationResult
from like.admin.schemas.system import (
    SystemLoginIn, SystemLogoutIn, SystemAuthAdminListIn, SystemAuthAdminDetailIn, SystemAuthAdminCreateIn,
    SystemAuthAdminDelIn, SystemAuthAdminDisableIn, SystemAuthAdminEditIn, SystemAuthAdminUpdateIn,
    SystemAuthRoleDetailIn, SystemAuthRoleDelIn, SystemAuthRoleCreateIn, SystemAuthRoleEditIn,
    SystemAuthMenuDetailIn, SystemAuthMenuCreateIn, SystemAuthMenuEditIn, SystemAuthMenuDelIn,
    SystemAuthAdminOut, SystemAuthRoleDetailOut, SystemAuthPostOut, SystemAuthPostAddIn, SystemAuthPostDetailIn,
    SystemAuthPostDelIn,
    SystemAuthPostEditIn, SystemAuthDeptDetailIn, SystemAuthDeptDeleteIn, SystemAuthDeptAddIn, SystemAuthDeptEditIn)
from like.admin.service.system.auth_admin import ISystemAuthAdminService, SystemAuthAdminService
from like.admin.service.system.auth_dept import ISystemAuthDeptService, SystemAuthDeptService
from like.admin.service.system.auth_menu import ISystemAuthMenuService, SystemAuthMenuService
from like.admin.service.system.auth_post import ISystemAuthPostService, SystemAuthPostService
from like.admin.service.system.auth_role import ISystemAuthRoleService, SystemAuthRoleService
from like.admin.service.system.login import ISystemLoginService, SystemLoginService
from like.dependencies.log import record_log
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


@router.post('/admin/add', dependencies=[Depends(record_log(title='管理员新增'))])
@unified_resp
async def admin_add(admin_create_in: SystemAuthAdminCreateIn,
                    auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员新增"""
    return await auth_service.add(admin_create_in)


@router.post('/admin/edit', dependencies=[Depends(record_log(title='管理员编辑'))])
@unified_resp
async def admin_edit(admin_edit_in: SystemAuthAdminEditIn,
                     auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员编辑"""
    return await auth_service.edit(admin_edit_in)


@router.post('/admin/upInfo', dependencies=[Depends(record_log(title='管理员更新'))])
@unified_resp
async def admin_upinfo(request: Request, admin_update_in: SystemAuthAdminUpdateIn,
                       auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员更新"""
    return await auth_service.update(admin_update_in, request.state.admin_id)


@router.post('/admin/del', dependencies=[Depends(record_log(title='管理员删除'))])
@unified_resp
async def admin_del(admin_del_in: SystemAuthAdminDelIn,
                    auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员删除"""
    return await auth_service.delete(admin_del_in.id)


@router.post('/admin/disable', dependencies=[Depends(record_log(title='管理员状态切换'))])
@unified_resp
async def admin_disable(admin_disable_in: SystemAuthAdminDisableIn,
                        auth_service: ISystemAuthAdminService = Depends(SystemAuthAdminService.instance)):
    """管理员状态切换"""
    return await auth_service.disable(admin_disable_in.id)


@router.get('/role/all')
@unified_resp
async def role_all(role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
    """角色所有"""
    return await role_service.all()


@router.get('/role/list', dependencies=[Depends(record_log(title='角色列表'))],
            response_model=PageInationResult[SystemAuthRoleDetailOut])
@unified_resp
async def role_list(role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
    """角色列表"""
    return await role_service.list()


@router.get('/role/detail', dependencies=[Depends(record_log(title='角色详情'))])
@unified_resp
async def role_detail(detail_in: SystemAuthRoleDetailIn = Depends(),
                      role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
    """角色详情"""
    return await role_service.detail(detail_in.id)


@router.post('/role/add', dependencies=[Depends(record_log(title='角色新增'))])
@unified_resp
async def role_add(create_in: SystemAuthRoleCreateIn,
                   role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
    """新增角色"""
    return await role_service.add(create_in)


@router.post('/role/edit', dependencies=[Depends(record_log(title='角色编辑'))])
@unified_resp
async def role_edit(edit_in: SystemAuthRoleEditIn,
                    role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
    """编辑角色"""
    return await role_service.edit(edit_in)


@router.post('/role/del', dependencies=[Depends(record_log(title='角色删除'))])
@unified_resp
async def role_del(del_in: SystemAuthRoleDelIn,
                   role_service: ISystemAuthRoleService = Depends(SystemAuthRoleService.instance)):
    """删除角色"""
    return await role_service.delete(del_in.id)


@router.get('/menu/route')
@unified_resp
async def menu_route(request: Request,
                     menu_service: ISystemAuthMenuService = Depends(SystemAuthMenuService.instance)):
    """菜单路由"""
    return await menu_service.select_menu_by_role_id(request.state.admin_id)


@router.get('/menu/list')
@unified_resp
async def menu_list(menu_service: ISystemAuthMenuService = Depends(SystemAuthMenuService.instance)):
    """菜单列表"""
    return await menu_service.list()


@router.get('/menu/detail')
@unified_resp
async def menu_detail(detail_in: SystemAuthMenuDetailIn = Depends(),
                      menu_service: ISystemAuthMenuService = Depends(SystemAuthMenuService.instance)):
    """菜单详情"""
    return await menu_service.detail(detail_in.id)


@router.post('/menu/add', dependencies=[Depends(record_log(title='菜单新增'))])
@unified_resp
async def menu_add(create_in: SystemAuthMenuCreateIn,
                   menu_service: ISystemAuthMenuService = Depends(SystemAuthMenuService.instance)):
    """新增菜单"""
    return await menu_service.add(create_in)


@router.post('/menu/edit', dependencies=[Depends(record_log(title='菜单编辑'))])
@unified_resp
async def menu_edit(edit_in: SystemAuthMenuEditIn,
                    menu_service: ISystemAuthMenuService = Depends(SystemAuthMenuService.instance)):
    """编辑菜单"""
    return await menu_service.edit(edit_in)


@router.post('/menu/del', dependencies=[Depends(record_log(title='菜单删除'))])
@unified_resp
async def menu_del(del_in: SystemAuthMenuDelIn,
                   menu_service: ISystemAuthMenuService = Depends(SystemAuthMenuService.instance)):
    """删除菜单"""
    return await menu_service.delete(del_in.id)


# 岗位相关接口
@router.get('/post/all')
@unified_resp
async def post_all(post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.fetch_all()


@router.get('/post/detail')
@unified_resp
async def post_detail(post_detail_in: SystemAuthPostDetailIn = Depends(),
                      post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.detail(post_detail_in.id)


@router.get('/post/list', response_model=PageInationResult[SystemAuthPostOut])
@unified_resp
async def post_list(code: Union[str, None] = Query(default=None), status: Union[int, None] = Query(default=None),
                    name: Union[str, None] = Query(default=None),
                    post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.fetch_list(code=code, name=name, is_stop=status)


@router.post('/post/add')
@unified_resp
async def post_add(post_add_in: SystemAuthPostAddIn = Depends(),
                   post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.add(post_add_in)


@router.post('/post/delete')
@unified_resp
async def post_delete(post_delete_in: SystemAuthPostDelIn = Depends(),
                      post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.delete(post_delete_in.id)


@router.post('/post/edit')
@unified_resp
async def post_edit(post_edit_in: SystemAuthPostEditIn = Depends(),
                    post_service: ISystemAuthPostService = Depends(SystemAuthPostService.instance)):
    return await post_service.edit(post_edit_in)


@router.get('/dept/all')
@unified_resp
async def dept_all(dept_service: ISystemAuthDeptService = Depends(SystemAuthDeptService.instance)):
    return await dept_service.fetch_all()


@router.get('/dept/list')
@unified_resp
async def dept_list(is_stop: Union[int, None] = Query(default=None),
                    name: Union[str, None] = Query(default=None),
                    dept_service: ISystemAuthDeptService = Depends(SystemAuthDeptService.instance)):
    return await dept_service.fetch_list(name=name, is_stop=is_stop)


@router.get('/dept/add')
@unified_resp
async def dept_add(dept_add_in: SystemAuthDeptAddIn = Depends(),
                   dept_service: ISystemAuthDeptService = Depends(SystemAuthDeptService.instance)):
    return await dept_service.add(dept_add_in)


@router.get('/dept/edit')
@unified_resp
async def dept_edit(dept_edit_in: SystemAuthDeptEditIn = Depends(),
                    dept_service: ISystemAuthDeptService = Depends(SystemAuthDeptService.instance)):
    return await dept_service.edit(dept_edit_in)


@router.get('/dept/detail')
@unified_resp
async def dept_detail(dept_detail_in: SystemAuthDeptDetailIn = Depends(),
                      post_service: ISystemAuthDeptService = Depends(SystemAuthDeptService.instance)):
    return await post_service.detail(dept_detail_in.id)


@router.get('/dept/delete')
@unified_resp
async def dept_delete(dept_deletel_in: SystemAuthDeptDeleteIn = Depends(),
                      post_service: ISystemAuthDeptService = Depends(SystemAuthDeptService.instance)):
    return await post_service.delete(dept_deletel_in.id)
