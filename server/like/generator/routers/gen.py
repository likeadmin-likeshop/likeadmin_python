from fastapi import APIRouter, Depends, Response

from like.generator.schemas.generate import (
    DbTablesIn, ListTableIn, DetailTableIn, ImportTableIn, SyncTableIn, DelTableIn, PreviewCodeIn,
    GenCodeIn, DownloadCodeIn, EditTableIn,
    DbTableOut, GenTableOut)
from like.generator.service.generate import IGenerateService, GenerateService
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter(prefix='/gen')


@router.get('/db', response_model=PageInationResult[DbTableOut])
@unified_resp
async def get_db(db_in: DbTablesIn = Depends(), gen_service: IGenerateService = Depends(GenerateService.instance)):
    """库表列表"""
    return await gen_service.db_tables(db_in)


@router.get('/list', response_model=PageInationResult[GenTableOut])
@unified_resp
async def get_list(list_in: ListTableIn = Depends(),
                   gen_service: IGenerateService = Depends(GenerateService.instance)):
    """生成列表"""
    return await gen_service.list(list_in)


@router.get('/detail')
@unified_resp
async def get_detail(detail_in: DetailTableIn = Depends(),
                     gen_service: IGenerateService = Depends(GenerateService.instance)):
    """生成详情"""
    return await gen_service.detail(detail_in.id)


@router.post('/importTable')
@unified_resp
async def import_table(import_in: ImportTableIn = Depends(),
                       gen_service: IGenerateService = Depends(GenerateService.instance)):
    """导入表结构"""
    assert import_in.tables, '请选择要导入的表'
    return await gen_service.import_table(import_in.tables.split(','))


@router.post('/editTable')
@unified_resp
async def edit_table(edit_in: EditTableIn,
                     gen_service: IGenerateService = Depends(GenerateService.instance)):
    """编辑表结构"""
    return await gen_service.edit_table(edit_in)


@router.post('/delTable')
@unified_resp
async def del_table(del_in: DelTableIn, gen_service: IGenerateService = Depends(GenerateService.instance)):
    """删除表结构"""
    return await gen_service.delete_table(del_in.ids)


@router.post('/syncTable')
@unified_resp
async def sync_table(sync_in: SyncTableIn = Depends(),
                     gen_service: IGenerateService = Depends(GenerateService.instance)):
    """同步表结构"""
    return await gen_service.sync_table(sync_in.id)


@router.get('/previewCode')
@unified_resp
async def preview_code(preview_in: PreviewCodeIn = Depends(),
                       gen_service: IGenerateService = Depends(GenerateService.instance)):
    """预览代码"""
    return await gen_service.preview_code(preview_in.id)


@router.get('/genCode')
@unified_resp
async def gen_code(gen_in: GenCodeIn = Depends(),
                   gen_service: IGenerateService = Depends(GenerateService.instance)):
    """生成代码"""
    assert gen_in.tables, '请选择要生成的表!'
    for table_name in gen_in.tables.split(','):
        await gen_service.gen_code(table_name)
    return


@router.get('/downloadCode')
async def download_code(download_in: DownloadCodeIn = Depends(),
                        gen_service: IGenerateService = Depends(GenerateService.instance)):
    """下载代码"""
    bio = await gen_service.download_code(download_in.tables.split(','))
    resp = Response(bio.getvalue(), media_type='application/x-zip-compressed',
                    headers={'Content-Disposition': 'attachment; filename=likeadmin-gen.zip'})
    return resp
