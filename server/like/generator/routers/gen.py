from fastapi import APIRouter, Depends

from like.generator.schemas.generate import DbTablesIn, ImportTableIn, PreviewCodeIn, GenCodeIn, DbTableOut
from like.generator.service.generate import IGenerateService, GenerateService
from like.http_base import unified_resp
from like.schema_base import PageInationResult

router = APIRouter(prefix='/gen')


@router.get('/db', response_model=PageInationResult[DbTableOut])
@unified_resp
async def get_db(db_in: DbTablesIn = Depends(), gen_service: IGenerateService = Depends(GenerateService.instance)):
    """库表列表"""
    return await gen_service.db_tables(db_in)


@router.get('/list')
@unified_resp
async def get_list():
    return


@router.get('/detail')
@unified_resp
async def get_detail():
    return


@router.post('/importTable')
@unified_resp
async def import_table(import_in: ImportTableIn = Depends(),
                       gen_service: IGenerateService = Depends(GenerateService.instance)):
    """导入表结构"""
    assert import_in.tables, '请选择要导入的表'
    return await gen_service.import_table(import_in.tables.split(','))


@router.post('/editTable')
@unified_resp
async def edit_table():
    return


@router.post('/delTable')
@unified_resp
async def del_table():
    return


@router.post('/syncTable')
@unified_resp
async def sync_table():
    return


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
@unified_resp
async def download_code():
    return
