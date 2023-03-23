from fastapi import APIRouter, Depends

from like.admin.schemas.article import ArticleCateListIn, ArticleCateOut, ArticleCateDetailIn, ArticleCateDeleteIn, \
    ArticleCateEditIn, ArticleCateAddIn, ArticleCateChangeIn, ArticleListIn, ArticleListOut, ArticleDetailIn, \
    ArticleAddIn, ArticleEditIn, ArticleChangeIn, ArticleDeleteIn
from like.admin.service.article.article import IArticleService, ArticleService
from like.admin.service.article.article_cate import IArticleCateService, ArticleCateService
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter(prefix='/article')


@router.get('/cate/all')
@unified_resp
async def cate_all(article_cate_service: IArticleCateService = Depends(ArticleCateService.instance)):
    """
    分类所有
    :param article_cate_service:
    :return:
    """
    return await article_cate_service.all()


@router.get('/cate/list', response_model=PageInationResult[ArticleCateOut])
@unified_resp
async def cate_list(list_in: ArticleCateListIn = Depends(),
                    article_cate_service: IArticleCateService = Depends(ArticleCateService.instance)):
    """
    分类列表
    :param list_in:
    :param article_cate_service:
    :return:
    """
    return await article_cate_service.list(list_in)


@router.get('/cate/detail')
@unified_resp
async def cate_detail(detail_in: ArticleCateDetailIn = Depends(),
                      article_cate_service: IArticleCateService = Depends(ArticleCateService.instance)):
    """
    分类新增
    :param detail_in:
    :param article_cate_service:
    :return:
    """
    return await article_cate_service.detail(detail_in)


@router.post('/cate/add')
@unified_resp
async def cate_add(add_in: ArticleCateAddIn,
                   article_cate_service: IArticleCateService = Depends(ArticleCateService.instance)):
    """
    分类新增
    :param add_in:
    :param article_cate_service:
    :return:
    """
    return await article_cate_service.add(add_in)


@router.post('/cate/edit')
@unified_resp
async def cate_edit(edit_in: ArticleCateEditIn,
                    article_cate_service: IArticleCateService = Depends(ArticleCateService.instance)):
    """
    分类修改
    :param edit_in:
    :param article_cate_service:
    :return:
    """
    return await article_cate_service.edit(edit_in)


@router.post('/cate/del')
@unified_resp
async def cate_del(del_in: ArticleCateDeleteIn,
                   article_cate_service: IArticleCateService = Depends(ArticleCateService.instance)):
    """
    分类删除
    :param del_in:
    :param article_cate_service:
    :return:
    """
    return await article_cate_service.delete(del_in)


@router.post('/cate/change')
@unified_resp
async def cate_change(change_in: ArticleCateChangeIn,
                      article_cate_service: IArticleCateService = Depends(ArticleCateService.instance)):
    """
    分类状态
    :param change_in:
    :param article_cate_service:
    :return:
    """
    return await article_cate_service.change(change_in)


@router.get('/list', response_model=PageInationResult[ArticleListOut])
@unified_resp
async def article_list(list_in: ArticleListIn = Depends(),
                       article_service: IArticleService = Depends(ArticleService.instance)):
    """
    文章列表
    :return:
    """
    return await article_service.list(list_in)


@router.get('/detail')
@unified_resp
async def article_detail(detail_in: ArticleDetailIn = Depends(),
                         article_service: IArticleService = Depends(ArticleService.instance)):
    """
    文章详情
    :return:
    """
    return await article_service.detail(detail_in)


@router.post('/add')
@unified_resp
async def article_add(add_in: ArticleAddIn, article_service: IArticleService = Depends(ArticleService.instance)):
    """
    添加文章
    :return:
    """
    return await article_service.add(add_in)


@router.post('/edit')
@unified_resp
async def article_edit(edit_in: ArticleEditIn, article_service: IArticleService = Depends(ArticleService.instance)):
    """
    修改文章
    :return:
    """
    return await article_service.edit(edit_in)


@router.post('/del')
@unified_resp
async def article_del(del_in: ArticleDeleteIn,
                      article_service: IArticleService = Depends(ArticleService.instance)):
    """
    文章删除
    :return:
    """
    return await article_service.delete(del_in)


@router.post('/change')
@unified_resp
async def article_change(change_in: ArticleChangeIn,
                         article_service: IArticleService = Depends(ArticleService.instance)):
    """
    修改文章状态
    :return:
    """
    return await article_service.change(change_in)
