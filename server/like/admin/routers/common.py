from fastapi import APIRouter, Depends, UploadFile, Form

from like.admin.schemas.common import CommonAlbumOut, CommonAlbumListIn, CommonAlbumCateListIn, CommonAlbumCateDelIn, \
    CommonAlbumRenameIn, CommonAlbumCateEditIn, CommonAlbumMoveIn, CommonAlbumDelIn
from like.admin.service.common.album import IAlbumService, AlbumService
from like.admin.service.common.index import IIndexService, IndexService
from like.admin.service.common.upload import IUploadService, UploadService
from like.dependencies.log import record_log, RequestType
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter(prefix='/common')


@router.get('/index/console')
@unified_resp
async def index_console(index_service: IIndexService = Depends(IndexService.instance)):
    """控制台"""
    return await index_service.console()


@router.get('/index/config')
@unified_resp
async def index_config(index_service: IIndexService = Depends(IndexService.instance)):
    """公共配置"""
    return await index_service.config()


@router.post('/album/albumRename', dependencies=[Depends(record_log(title='相册文件重命名'))])
@unified_resp
async def album_rename(params: CommonAlbumRenameIn, common_service: IAlbumService = Depends(AlbumService.instance)):
    """文件命名"""
    return await common_service.album_rename(params)


@router.post('/album/albumMove', dependencies=[Depends(record_log(title='相册文件移动'))])
@unified_resp
async def album_move(params: CommonAlbumMoveIn, common_service: IAlbumService = Depends(AlbumService.instance)):
    """文件移动"""
    return await common_service.album_move(params)


@router.post('/album/albumDel', dependencies=[Depends(record_log(title='相册文件删除'))])
@unified_resp
async def album_del(params: CommonAlbumDelIn, common_service: IAlbumService = Depends(AlbumService.instance)):
    """文件删除"""
    return await common_service.album_del(params)


@router.get('/album/albumList', response_model=PageInationResult[CommonAlbumOut])
@unified_resp
async def album_list(params: CommonAlbumListIn = Depends(),
                     common_service: IAlbumService = Depends(AlbumService.instance)):
    """文件列表"""
    return await common_service.album_list(params)


@router.post('/album/cateRename', dependencies=[Depends(record_log(title='相册分类重命名'))])
@unified_resp
async def cate_rename(params: CommonAlbumRenameIn, common_service: IAlbumService = Depends(AlbumService.instance)):
    """类目命名"""
    return await common_service.cate_rename(params)


@router.post('/album/cateAdd', dependencies=[Depends(record_log(title='相册分类新增'))])
@unified_resp
async def cate_add(params: CommonAlbumCateEditIn, common_service: IAlbumService = Depends(AlbumService.instance)):
    """类目新增"""
    return await common_service.cate_add(params)


@router.post('/album/cateDel', dependencies=[Depends(record_log(title='相册分类删除'))])
@unified_resp
async def cate_del(params: CommonAlbumCateDelIn, common_service: IAlbumService = Depends(AlbumService.instance)):
    """类目删除"""
    return await common_service.cate_del(params)


@router.get('/album/cateList')
@unified_resp
async def cate_list(params: CommonAlbumCateListIn = Depends(),
                    common_service: IAlbumService = Depends(AlbumService.instance)):
    """类目列表"""
    return await common_service.cate_list(params)


@router.post('/upload/image', dependencies=[Depends(record_log(title='上传图片', req_type=RequestType.File))])
@unified_resp
async def upload_image(file: UploadFile, cid: int = Form(default=0),
                       upload_service: IUploadService = Depends(UploadService.instance)):
    """上传图片"""
    return await upload_service.upload_image(file, cid)


@router.post('/upload/video', dependencies=[Depends(record_log(title='上传视频', req_type=RequestType.File))])
@unified_resp
async def upload_video(file: UploadFile, cid: int = Form(default=0),
                       upload_service: IUploadService = Depends(UploadService.instance)):
    """上传视频"""
    return await upload_service.upload_video(file, cid)
