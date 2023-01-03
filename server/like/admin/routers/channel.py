from fastapi import APIRouter, Depends

from like.admin.schemas.channel import ChannelOaIn
from like.admin.service.channel.oa import IChannelOaService, ChannelOaService
from like.http_base import unified_resp

router = APIRouter(prefix='/channel')


@router.get('/oa/detail')
@unified_resp
async def oa_detail(oa_service: IChannelOaService = Depends(ChannelOaService.instance)):
    """公众号渠道设置详情"""
    return await oa_service.detail()


@router.post('/oa/save')
@unified_resp
async def oa_save(os_in: ChannelOaIn, oa_service: IChannelOaService = Depends(ChannelOaService.instance)):
    """公众号渠道设置保存"""
    return await oa_service.save(os_in)
