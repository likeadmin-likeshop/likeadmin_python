from fastapi import APIRouter, Depends

from like.generator.schemas.generate import DbTablesIn, DbTableOut
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
async def import_table():
    return


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


@router.post('/previewCode')
@unified_resp
async def preview_code():
    return


@router.post('/genCode')
@unified_resp
async def gen_code():
    return


@router.post('/downloadCode')
@unified_resp
async def download_code():
    return
