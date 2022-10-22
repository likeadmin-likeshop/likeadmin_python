from typing import Final, Optional

from redis import asyncio as aioredis
from starlette.requests import Request
from starlette.responses import Response
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

from ..config import get_settings

redis_be: Final[RedisBackend] = RedisBackend(
    aioredis.from_url(get_settings().redis_url, encoding='utf8', decode_responses=True))


def custom_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
):
    key = kwargs.get('key')
    if not key and args:
        key = args[0]
    cache_key = f'{FastAPICache.get_prefix()}{str(key)}'
    return cache_key
