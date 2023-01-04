from fastapi import APIRouter, Depends

from like.admin.schemas.channel import ChannelOaIn, ChannelOaMenusIn
from like.admin.service.channel.oa import IChannelOaService, ChannelOaService
from like.admin.service.channel.oa_menu import IChannelOaMenuService, ChannelOaMenuService
from like.http_base import unified_resp

router = APIRouter(prefix='/channel')


@router.get('/oa/detail')
@unified_resp
async def oa_detail(oa_service: IChannelOaService = Depends(ChannelOaService.instance)):
    """公众号渠道设置详情"""
    return await oa_service.detail()


@router.post('/oa/save')
@unified_resp
async def oa_save(oa_in: ChannelOaIn, oa_service: IChannelOaService = Depends(ChannelOaService.instance)):
    """公众号渠道设置保存"""
    return await oa_service.save(oa_in)


@router.get('/oaMenu/detail')
@unified_resp
async def oa_menu_detail(menu_service: IChannelOaMenuService = Depends(ChannelOaMenuService.instance)):
    """公众号菜单详情"""
    return await menu_service.detail()


@router.post('/oaMenu/save')
@unified_resp
async def oa_menu_save(menus_in: ChannelOaMenusIn,
                       menu_service: IChannelOaMenuService = Depends(ChannelOaMenuService.instance)):
    """公众号仅是保存菜单"""
    return await menu_service.save(menus_in, False)


@router.post('/oaMenu/publish')
@unified_resp
async def oa_menu_publish(menus_in: ChannelOaMenusIn,
                          menu_service: IChannelOaMenuService = Depends(ChannelOaMenuService.instance)):
    """公众号保存并发布菜单"""
    return await menu_service.save(menus_in, True)
