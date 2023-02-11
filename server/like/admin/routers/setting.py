import logging

from fastapi import APIRouter, Depends

from like.admin.schemas.setting import (
    SettingWebsiteIn, SettingCopyrightIn, SettingProtocolIn, SettingStorageDetailIn,
    SettingStorageEditIn, SettingStorageChangeIn, SettingDictTypeOut, SettingDictTypeListIn, SettingDictTypeAddIn,
    SettingDictTypeEditIn, SettingDictTypeDeleteIn, SettingDictTypeDetailIn, SettingDictDataListIn,
    SettingDictDataDetailIn, SettingDictDataAddIn, SettingDictDataEditIn, SettingDictDataDeletelIn, SettingDictDataOut,
    SettingHotSearchIn, SettingLoginIn, SettingUserIn, SettingSmsDetailIn, SettingSmsSaveIn)
from like.admin.service.setting.copyright import ISettingCopyrightService, SettingCopyrightService
from like.admin.service.setting.dict_manager import SettingDictTypeService, ISettingDictTypeService, \
    SettingDictDataService, ISettingDictDataService
from like.admin.service.setting.login import ISettingLoginService, SettingLoginService
from like.admin.service.setting.protocol import ISettingProtocolService, SettingProtocolService
from like.admin.service.setting.search import ISettingSearchService, SettingSearchService
from like.admin.service.setting.sms import ISettingSmsService, SettingSmsService
from like.admin.service.setting.storage_service import SettingStorageService, ISettingStorageService
from like.admin.service.setting.user import ISettingUserService, SettingUserService
from like.admin.service.setting.website import ISettingWebsiteService, SettingWebsiteService
from like.http_base import unified_resp
from like.schema_base import PageInationResult

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
async def storage_list(service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.list()


@router.get('/storage/detail')
@unified_resp
async def storage_detail(storage_detail_in: SettingStorageDetailIn = Depends(),
                         service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.detail(storage_detail_in.alias)


@router.post('/storage/edit')
@unified_resp
async def storage_edit(storage_edit_in: SettingStorageEditIn,
                       service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.edit(storage_edit_in)


@router.post('/storage/change')
@unified_resp
async def storage_change(storage_change_in: SettingStorageChangeIn,
                         service: ISettingStorageService = Depends(SettingStorageService.instance)):
    return await service.change(storage_change_in.alias, storage_change_in.status)


@router.get('/dict/type/all')
@unified_resp
async def dict_type_all(service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
    return await service.all()


@router.get('/dict/type/list', response_model=PageInationResult[SettingDictTypeOut])
@unified_resp
async def dict_type_list(list_in: SettingDictTypeListIn = Depends(),
                         service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
    return await service.list(list_in)


@router.get('/dict/type/detail')
@unified_resp
async def dict_type_detail(detail_in: SettingDictTypeDetailIn = Depends(),
                           service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
    return await service.detail(detail_in)


@router.post('/dict/type/add')
@unified_resp
async def dict_type_add(add_in: SettingDictTypeAddIn,
                        service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
    return await service.add(add_in)


@router.post('/dict/type/edit')
@unified_resp
async def dict_type_edit(edit_in: SettingDictTypeEditIn,
                         service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
    return await service.edit(edit_in)


@router.post('/dict/type/del')
@unified_resp
async def dict_type_del(delete_in: SettingDictTypeDeleteIn,
                        service: ISettingDictTypeService = Depends(SettingDictTypeService.instance)):
    return await service.delete(delete_in)


@router.get('/dict/data/all')
@unified_resp
async def dict_data_all(all_in: SettingDictDataListIn = Depends(),
                        service: ISettingDictDataService = Depends(SettingDictDataService.instance)):
    return await service.all(all_in)


@router.get('/dict/data/list', response_model=PageInationResult[SettingDictDataOut])
@unified_resp
async def dict_data_list(list_in: SettingDictDataListIn = Depends(),
                         service: ISettingDictDataService = Depends(SettingDictDataService.instance)):
    return await service.list(list_in)


@router.get('/dict/data/detail')
@unified_resp
async def dict_data_detail(detail_in: SettingDictDataDetailIn = Depends(),
                           service: ISettingDictDataService = Depends(SettingDictDataService.instance)):
    return await service.detail(detail_in)


@router.post('/dict/data/add')
@unified_resp
async def dict_data_add(add_in: SettingDictDataAddIn,
                        service: ISettingDictDataService = Depends(SettingDictDataService.instance)):
    return await service.add(add_in)


@router.post('/dict/data/edit')
@unified_resp
async def dict_data_edit(edit_in: SettingDictDataEditIn,
                         service: ISettingDictDataService = Depends(SettingDictDataService.instance)):
    return await service.edit(edit_in)


@router.post('/dict/data/del')
@unified_resp
async def dict_data_del(delete_in: SettingDictDataDeletelIn,
                        service: ISettingDictDataService = Depends(SettingDictDataService.instance)):
    return await service.delete(delete_in)


@router.get('/search/detail')
@unified_resp
async def search_detail(search_service: ISettingSearchService = Depends(SettingSearchService.instance)):
    """热门搜索详情"""
    return await search_service.detail()


@router.post('/search/save')
@unified_resp
async def search_save(hot_search_in: SettingHotSearchIn,
                      search_service: ISettingSearchService = Depends(SettingSearchService.instance)):
    """热门搜索保存"""
    return await search_service.save(hot_search_in)


@router.get('/login/detail')
@unified_resp
async def login_detail(login_service: ISettingLoginService = Depends(SettingLoginService.instance)):
    """登录设置详情"""
    return await login_service.detail()


@router.post('/login/save')
@unified_resp
async def login_save(login_in: SettingLoginIn,
                     login_service: ISettingLoginService = Depends(SettingLoginService.instance)):
    """登录设置保存"""
    return await login_service.save(login_in)


@router.get('/user/detail')
@unified_resp
async def user_detail(user_service: ISettingUserService = Depends(SettingUserService.instance)):
    """用户设置详情"""
    return await user_service.detail()


@router.post('/user/save')
@unified_resp
async def user_save(user_in: SettingUserIn,
                    user_service: ISettingUserService = Depends(SettingUserService.instance)):
    """用户设置保存"""
    return await user_service.save(user_in)


@router.get('/sms/list')
@unified_resp
async def sms_list(sms_service: ISettingSmsService = Depends(SettingSmsService.instance)):
    """短信引擎列表"""
    return await sms_service.list()


@router.get('/sms/detail')
@unified_resp
async def sms_detail(detail_in: SettingSmsDetailIn = Depends(),
                     sms_service: ISettingSmsService = Depends(SettingSmsService.instance)):
    """短信引擎详情"""
    return await sms_service.detail(detail_in.alias)


@router.post('/sms/save')
@unified_resp
async def sms_save(save_in: SettingSmsSaveIn,
                   sms_service: ISettingSmsService = Depends(SettingSmsService.instance)):
    """短信引擎保存"""
    return await sms_service.save(save_in)
