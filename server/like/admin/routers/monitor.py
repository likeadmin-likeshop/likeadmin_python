import logging

from fastapi import APIRouter, Depends

from like.dependencies.log import record_log
from like.http_base import unified_resp
from like.utils.redis import RedisUtil

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/monitor')


@router.get('/cache', dependencies=[Depends(record_log(title='缓存监控'))])
@unified_resp
async def monitor_cache():
    """缓存监控"""
    info = await RedisUtil.info()
    res_info = {}
    for key, value in info.items():
        if isinstance(value, dict):
            value = ','.join({f'{k}={v}' for k, v in value.items()})
        else:
            value = str(value)
        res_info[key] = value

    db_size = await RedisUtil.dbsize()

    command_stats = await RedisUtil.info('commandstats')
    stats_list = []
    for k, v in command_stats.items():
        stats_list.append({'name': k.split('_')[-1], 'value': str(v.get('calls', ''))})
    return {'info': res_info, 'commandStats': stats_list, 'dbSize': db_size}
