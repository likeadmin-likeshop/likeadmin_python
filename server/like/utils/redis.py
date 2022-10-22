from typing import Final, Union, Awaitable, Set

from redis import Redis

from like.dependencies.cache import redis_be
from ..config import get_settings

__all__ = ['RedisUtil']

Field = Union[int, float, str]


class RedisUtil:
    prefix: Final[str] = get_settings().redis_prefix
    redis: Final[Redis] = redis_be.redis

    @staticmethod
    def get_key(key: str) -> str:
        return f'{RedisUtil.prefix}{key}'

    @classmethod
    def set(cls, key: str, value: Field, time: int = None) -> Awaitable:
        return RedisUtil.redis.set(cls.get_key(key), value=value, ex=time)

    @classmethod
    def sset(cls, key: str, *values: Field) -> Awaitable[int]:
        return RedisUtil.redis.sadd(cls.get_key(key), *values)

    @classmethod
    def sget(cls, key: str) -> Awaitable[Set]:
        return RedisUtil.redis.smembers(cls.get_key(key))

    @classmethod
    def delete(cls, *keys: str) -> Awaitable:
        return RedisUtil.redis.delete(*(cls.get_key(key) for key in keys))
