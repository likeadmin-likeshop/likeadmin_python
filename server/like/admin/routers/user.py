from fastapi import APIRouter

from like.models import users
from like.http_base import unified_resp
from like.dependencies.database import db

router = APIRouter(prefix='/user')


@router.get('/list')
@unified_resp
async def user_list():
    query = users.select()
    return await db.fetch_all(query)
