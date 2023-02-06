from fastapi import APIRouter, Depends

from like.admin.schemas.channel import ChannelOaIn, ChannelOaMenusIn, ChannelH5In, ChannelMpIn
from like.admin.service.channel.h5 import IChannelH5Service, ChannelH5Service
from like.admin.service.channel.mp import IChannelMpService, ChannelMpService
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


@router.get('/h5/detail')
@unified_resp
async def h5_detail(h5_service: IChannelH5Service = Depends(ChannelH5Service.instance)):
    """H5渠道设置详情"""
    return await h5_service.detail()


@router.post('/h5/save')
@unified_resp
async def h5_save(h5_in: ChannelH5In, h5_service: IChannelH5Service = Depends(ChannelH5Service.instance)):
    """H5渠道设置保存"""
    return await h5_service.save(h5_in)


@router.get('/mp/detail')
@unified_resp
async def mp_detail(mp_service: IChannelMpService = Depends(ChannelMpService.instance)):
    """微信小程序渠道设置详情"""
    return await mp_service.detail()


@router.post('/mp/save')
@unified_resp
async def mp_save(mp_in: ChannelMpIn, mp_service: IChannelMpService = Depends(ChannelMpService.instance)):
    """微信小程序渠道设置保存"""
    return await mp_service.save(mp_in)
