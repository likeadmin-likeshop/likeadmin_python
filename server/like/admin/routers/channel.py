from fastapi import APIRouter, Depends

from like.admin.schemas.channel import (
    ChannelOaIn, ChannelOaMenusIn, ChannelH5In, ChannelMpIn, ChannelWxIn, ChannelOaReplyDefaultDetailIn,
    ChannelOaReplyDefaultCreateIn, ChannelOaReplyDefaultEditIn, ChannelOaReplyDefaultDelIn,
    ChannelOaReplyDefaultStatusIn, ChannelOaReplyFollowDetailIn, ChannelOaReplyFollowCreateIn,
    ChannelOaReplyFollowEditIn, ChannelOaReplyFollowDelIn, ChannelOaReplyFollowStatusIn,
    ChannelOaReplyOut)
from like.admin.service.channel.h5 import IChannelH5Service, ChannelH5Service
from like.admin.service.channel.mp import IChannelMpService, ChannelMpService
from like.admin.service.channel.oa import IChannelOaService, ChannelOaService
from like.admin.service.channel.oa_menu import IChannelOaMenuService, ChannelOaMenuService
from like.admin.service.channel.oa_reply_default import IChannelOaReplyDefaultService, ChannelOaReplyDefaultService
from like.admin.service.channel.oa_reply_follow import IChannelOaReplyFollowService, ChannelOaReplyFollowService
from like.admin.service.channel.wx import IChannelWxService, ChannelWxService
from like.dependencies.log import record_log
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter(prefix='/channel')


@router.get('/oa/detail')
@unified_resp
async def oa_detail(oa_service: IChannelOaService = Depends(ChannelOaService.instance)):
    """公众号渠道设置详情"""
    return await oa_service.detail()


@router.post('/oa/save', dependencies=[Depends(record_log(title='公众号渠道设置保存'))])
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


@router.post('/h5/save', dependencies=[Depends(record_log(title='H5渠道设置保存'))])
@unified_resp
async def h5_save(h5_in: ChannelH5In, h5_service: IChannelH5Service = Depends(ChannelH5Service.instance)):
    """H5渠道设置保存"""
    return await h5_service.save(h5_in)


@router.get('/mp/detail')
@unified_resp
async def mp_detail(mp_service: IChannelMpService = Depends(ChannelMpService.instance)):
    """微信小程序渠道设置详情"""
    return await mp_service.detail()


@router.post('/mp/save', dependencies=[Depends(record_log(title='微信小程序渠道设置保存'))])
@unified_resp
async def mp_save(mp_in: ChannelMpIn, mp_service: IChannelMpService = Depends(ChannelMpService.instance)):
    """微信小程序渠道设置保存"""
    return await mp_service.save(mp_in)


@router.get('/wx/detail')
@unified_resp
async def wx_detail(wx_service: IChannelWxService = Depends(ChannelWxService.instance)):
    """开放平台渠道设置详情"""
    return await wx_service.detail()


@router.post('/wx/save', dependencies=[Depends(record_log(title='开放平台渠道设置保存'))])
@unified_resp
async def wx_save(wx_in: ChannelWxIn, wx_service: IChannelWxService = Depends(ChannelWxService.instance)):
    """开放平台渠道设置保存"""
    return await wx_service.save(wx_in)


@router.get('/oaReplyDefault/list', response_model=PageInationResult[ChannelOaReplyOut])
@unified_resp
async def oa_reply_default_list(
        ord_service: IChannelOaReplyDefaultService = Depends(ChannelOaReplyDefaultService.instance)):
    """公众号默认回复列表"""
    return await ord_service.list()


@router.get('/oaReplyDefault/detail')
@unified_resp
async def oa_reply_default_detail(
        detail_in: ChannelOaReplyDefaultDetailIn = Depends(),
        ord_service: IChannelOaReplyDefaultService = Depends(ChannelOaReplyDefaultService.instance)):
    """公众号默认回复详情"""
    return await ord_service.detail(detail_in.id)


@router.post('/oaReplyDefault/add')
@unified_resp
async def oa_reply_default_add(
        create_in: ChannelOaReplyDefaultCreateIn,
        ord_service: IChannelOaReplyDefaultService = Depends(ChannelOaReplyDefaultService.instance)):
    """公众号默认回复新增"""
    return await ord_service.add(create_in)


@router.post('/oaReplyDefault/edit')
@unified_resp
async def oa_reply_default_edit(
        edit_in: ChannelOaReplyDefaultEditIn,
        ord_service: IChannelOaReplyDefaultService = Depends(ChannelOaReplyDefaultService.instance)):
    """公众号默认回复编辑"""
    return await ord_service.edit(edit_in)


@router.post('/oaReplyDefault/del')
@unified_resp
async def oa_reply_default_del(
        del_in: ChannelOaReplyDefaultDelIn,
        ord_service: IChannelOaReplyDefaultService = Depends(ChannelOaReplyDefaultService.instance)):
    """公众号默认回复删除"""
    return await ord_service.delete(del_in.id)


@router.post('/oaReplyDefault/status')
@unified_resp
async def oa_reply_default_status(
        status_in: ChannelOaReplyDefaultStatusIn,
        ord_service: IChannelOaReplyDefaultService = Depends(ChannelOaReplyDefaultService.instance)):
    """公众号默认回复状态"""
    return await ord_service.status(status_in.id)


@router.get('/oaReplyFollow/list', response_model=PageInationResult[ChannelOaReplyOut])
@unified_resp
async def oa_reply_follow_list(
        orf_service: IChannelOaReplyFollowService = Depends(ChannelOaReplyFollowService.instance)):
    """公众号关注回复列表"""
    return await orf_service.list()


@router.get('/oaReplyFollow/detail')
@unified_resp
async def oa_reply_follow_detail(
        detail_in: ChannelOaReplyFollowDetailIn = Depends(),
        orf_service: IChannelOaReplyFollowService = Depends(ChannelOaReplyFollowService.instance)):
    """公众号关注回复详情"""
    return await orf_service.detail(detail_in.id)


@router.post('/oaReplyFollow/add')
@unified_resp
async def oa_reply_follow_add(
        create_in: ChannelOaReplyFollowCreateIn,
        orf_service: IChannelOaReplyFollowService = Depends(ChannelOaReplyFollowService.instance)):
    """公众号关注回复新增"""
    return await orf_service.add(create_in)


@router.post('/oaReplyFollow/edit')
@unified_resp
async def oa_reply_follow_edit(
        edit_in: ChannelOaReplyFollowEditIn,
        orf_service: IChannelOaReplyFollowService = Depends(ChannelOaReplyFollowService.instance)):
    """公众号关注回复编辑"""
    return await orf_service.edit(edit_in)


@router.post('/oaReplyFollow/del')
@unified_resp
async def oa_reply_follow_del(
        del_in: ChannelOaReplyFollowDelIn,
        orf_service: IChannelOaReplyFollowService = Depends(ChannelOaReplyFollowService.instance)):
    """公众号关注回复删除"""
    return await orf_service.delete(del_in.id)


@router.post('/oaReplyFollow/status')
@unified_resp
async def oa_reply_follow_status(
        status_in: ChannelOaReplyFollowStatusIn,
        orf_service: IChannelOaReplyFollowService = Depends(ChannelOaReplyFollowService.instance)):
    """公众号关注回复状态"""
    return await orf_service.status(status_in.id)
