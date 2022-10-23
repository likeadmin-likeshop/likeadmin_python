from typing import Final, Union, Set, Any

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
    async def set(cls, key: str, value: Field, time: int = None):
        await RedisUtil.redis.set(cls.get_key(key), value=value, ex=time)

    @classmethod
    async def get(cls, key: str) -> str:
        return await RedisUtil.redis.get(cls.get_key(key))

    @classmethod
    async def exists(cls, *keys: str) -> int:
        return await RedisUtil.redis.exists(*(cls.get_key(key) for key in keys))

    @classmethod
    async def sset(cls, key: str, *values: Field) -> int:
        return await RedisUtil.redis.sadd(cls.get_key(key), *values)

    @classmethod
    async def sget(cls, key: str) -> Set:
        return await RedisUtil.redis.smembers(cls.get_key(key))

    @classmethod
    async def hmset(cls, key: str, mapping: dict, time: int = None) -> int:
        cnt = await RedisUtil.redis.hset(cls.get_key(key), mapping=mapping)
        if time and time > 0:
            await cls.expire(key, time)
        return cnt

    @classmethod
    async def hset(cls, key: str, field: str, value: Field, time: int = None) -> int:
        return await cls.hmset(cls.get_key(key), mapping={field: value}, time=time)

    @classmethod
    async def hget(cls, key: str, field: str) -> str:
        return await RedisUtil.redis.hget(cls.get_key(key), field)

    @classmethod
    async def hexists(cls, key: str, field: str) -> bool:
        return await RedisUtil.redis.hexists(cls.get_key(key), field)

    @classmethod
    async def hdel(cls, key: str, *fields: str) -> int:
        return await RedisUtil.redis.hdel(cls.get_key(key), *fields)

    @classmethod
    async def ttl(cls, key: str) -> int:
        return await RedisUtil.redis.ttl(cls.get_key(key))

    @classmethod
    async def expire(cls, key: str, time: int):
        await RedisUtil.redis.expire(cls.get_key(key), time)

    @classmethod
    async def delete(cls, *keys: str):
        await RedisUtil.redis.delete(*(cls.get_key(key) for key in keys))
