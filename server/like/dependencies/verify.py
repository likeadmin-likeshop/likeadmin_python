import json
from fastapi import Request


async def verify_token(request: Request):
    from like.utils.redis import RedisUtil
    from like.exceptions.base import AppException
    from like.admin.config import AdminConfig
    from like.http_base import HttpResp
    from like.admin.service.system.auth_admin import SystemAuthAdminService

    auths = request.url.path.replace('/api/', '').replace('/', ':')

    if auths in AdminConfig.not_login_uri:
        return

    token = request.headers.get('token', '')
    if not token:
        raise AppException(HttpResp.TOKEN_EMPTY)

    token = f'{AdminConfig.backstage_token_key}{token}'
    exist_cnt = await RedisUtil.exists(token)
    if exist_cnt == 0:
        raise AppException(HttpResp.TOKEN_INVALID)

    uid_str = await RedisUtil.get(token)
    uid = int(uid_str)
    if not await RedisUtil.hexists(AdminConfig.backstage_manage_key, uid_str):
        await SystemAuthAdminService.cache_admin_user_by_uid(uid_str)

    mapping = json.loads(await RedisUtil.hget(AdminConfig.backstage_manage_key, uid_str))
    if not (mapping and mapping.get('is_delete') == 0):
        await RedisUtil.delete(token)
        await RedisUtil.hdel(f'{AdminConfig.backstage_manage_key}{uid}')
        raise AppException(HttpResp.TOKEN_INVALID)

    if mapping.get('is_disable') == 1:
        raise AppException(HttpResp.LOGIN_DISABLE_ERROR)

    if await RedisUtil.ttl(token) < 1800:
        await RedisUtil.expire(token, 7200)

    request.state.admin_id = uid
    request.state.role_id = mapping.get('role')
    request.state.username = mapping.get('username')
    request.state.nickname = mapping.get('nickname')

    if auths in AdminConfig.not_auth_uri or uid == 1:
        return

    role_id = mapping.get('role')
    if not await RedisUtil.hexists(AdminConfig.backstage_roles_key, role_id):
        # TODO: cache role menus
        pass

    menus = await RedisUtil.hget(AdminConfig.backstage_roles_key, role_id)
    if not (menus and auths in menus.split(',')):
        raise AppException(HttpResp.NO_PERMISSION)
