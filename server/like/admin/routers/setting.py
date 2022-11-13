import logging

from fastapi import APIRouter, Depends

from like.admin.schemas.setting import SettingWebsiteIn, SettingCopyrightIn, SettingProtocolIn, SettingsStorageDetailIn, \
    SettingsStorageEditIn, SettingsStorageChangeIn
from like.admin.service.setting.copyright import ISettingCopyrightService, SettingCopyrightService
from like.admin.service.setting.protocol import ISettingProtocolService, SettingProtocolService
from like.admin.service.setting.storage_service import SettingStorageService, ISettingStorageService
from like.admin.service.setting.website import ISettingWebsiteService, SettingWebsiteService
from like.http_base import unified_resp

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/setting')


@router.get('/website/detail')
@unified_resp
async def website_detail(website_service: ISettingWebsiteService = Depends(SettingWebsiteService.instance)):
    """获取网站配置信息"""
    return await website_service.detail()


@router.post('/website/save')
@unified_resp
async def website_save(website_in: SettingWebsiteIn,
                       website_service: ISettingWebsiteService = Depends(SettingWebsiteService.instance)):
    """保存网站配置信息"""
    return await website_service.save(website_in)


@router.get('/copyright/detail')
@unified_resp
async def copyright_detail(copyright_service: ISettingCopyrightService = Depends(SettingCopyrightService.instance)):
    """获取网站备案信息"""
    return await copyright_service.detail()


@router.post('/copyright/save')
@unified_resp
async def copyright_save(copyright_in: SettingCopyrightIn,
                         copyright_service: ISettingCopyrightService = Depends(SettingCopyrightService.instance)):
    """保存网站备案信息"""
    return await copyright_service.save(copyright_in)


@router.get('/protocol/detail')
@unified_resp
async def protocol_detail(protocol_service: ISettingProtocolService = Depends(SettingProtocolService.instance)):
    """获取网站政策信息"""
    return await protocol_service.detail()


@router.post('/protocol/save')
@unified_resp
async def protocol_save(protocol_in: SettingProtocolIn,
                        protocol_service: ISettingProtocolService = Depends(SettingProtocolService.instance)):
    """保存网站政策信息"""
    return await protocol_service.save(protocol_in)


@router.get('/storage/list')
@unified_resp
async def list(service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.list()


@router.get('/storage/detail')
@unified_resp
async def detail(storage_detail_in: SettingsStorageDetailIn = Depends(),
                 service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.detail(storage_detail_in.alias)


@router.post('/storage/edit')
@unified_resp
async def edit(storage_edit_in: SettingsStorageEditIn = Depends(),
               service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.edit(storage_edit_in)


@router.post('/storage/change')
@unified_resp
async def change(storage_change_in: SettingsStorageChangeIn = Depends(),
                 service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.change(storage_change_in.alias, storage_change_in.status)
