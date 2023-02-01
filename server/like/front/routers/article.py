from fastapi import APIRouter, Depends

from like.front.schemas.article import ArticleListIn, ArticleDetailIn, ArticleBaseOut, ArticleCollectPostIn, \
    ArticleCollectOut
from like.front.service.article import IArticleService, ArticleService
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter(prefix='/article')


@router.get('/category')
@unified_resp
async def category(article_service: IArticleService = Depends(ArticleService.instance)):
    """
    分类
    :param article_service:
    :return:
    """
    return await article_service.category()


@router.get('/list', response_model=PageInationResult[ArticleBaseOut])
@unified_resp
async def article_list(list_in: ArticleListIn = Depends(),
                       article_service: IArticleService = Depends(ArticleService.instance)
                       ):
    """
    文章列表
    :param article_service:
    :return:
    """
    return await article_service.list(list_in)


@router.get('/detail')
@unified_resp
async def detail(detail_in: ArticleDetailIn = Depends(),
                 article_service: IArticleService = Depends(ArticleService.instance)):
    """
    文章详情
    :param detail_in:
    :param article_service:
    :return:
    """
    return await article_service.detail(detail_in)


@router.get('/collect', response_model=PageInationResult[ArticleCollectOut])
@unified_resp
async def collect(article_service: IArticleService = Depends(ArticleService.instance)):
    """
    收藏列表
    :param article_service:
    :return:
    """
    return await article_service.collect()


@router.post('/addCollect')
@unified_resp
async def collect(post_in: ArticleCollectPostIn, article_service: IArticleService = Depends(ArticleService.instance)):
    """
    添加收藏
    :param article_service:
    :return:
    """
    return await article_service.add_collect(post_in=post_in)


@router.post('/cancelCollect')
@unified_resp
async def collect(post_in: ArticleCollectPostIn, article_service: IArticleService = Depends(ArticleService.instance)):
    """
    取消收藏
    :param article_service:
    :return:
    """
    return await article_service.cancel_collect(post_in=post_in)
