"""
页面装修
"""

from fastapi import APIRouter, Depends

from like.admin.schemas.decorate import DecoratePageSaveIn, DecorateDataArticleIn, DecorateTabbarSaveIn
from like.admin.service.decorate.data_article import IDecorateArticleService, DecorateArticleService
from like.admin.service.decorate.page import IDecoratePageService, DecoratePageService
from like.admin.service.decorate.tabbar import IDecorateTabbarService, DecorateTabbarService
from like.http_base import unified_resp

router = APIRouter(prefix='/decorate')


@router.post('/pages/save')
@unified_resp
async def pages_save(save_in: DecoratePageSaveIn,
                     decorate_page_service: IDecoratePageService = Depends(DecoratePageService.instance)):
    """
     页面装修保存
    :return:
    """
    return await decorate_page_service.save(save_in)


@router.get('/pages/detail')
@unified_resp
async def pages_detail(id: int, decorate_page_service: IDecoratePageService = Depends(DecoratePageService.instance)):
    """
    页面装修详情
    :return:
    """
    return await decorate_page_service.detail(id)


@router.get('/tabbar/detail')
@unified_resp
async def tabbar_detail(tabbar_service: IDecorateTabbarService = Depends(DecorateTabbarService.instance)):
    """
    底部导航详情
    :return:
    """
    return await tabbar_service.detail()


@router.post('/tabbar/save')
@unified_resp
async def tabbar_save(save_in: DecorateTabbarSaveIn,
                      tabbar_service: IDecorateTabbarService = Depends(DecorateTabbarService.instance)):
    """
    底部导航保存
    :return:
    """
    return await tabbar_service.save(save_in)


@router.get('/data/article')
@unified_resp
async def data_article(article_in: DecorateDataArticleIn = Depends(),
                       decorate_article_service: IDecorateArticleService = Depends(DecorateArticleService.instance)):
    """
    获取文章数据
    :return:
    """
    return await decorate_article_service.data_article(article_in=article_in)
