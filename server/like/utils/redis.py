from typing import Union, Set

from redis import Redis

from like.dependencies.cache import redis_be
from ..config import get_settings

__all__ = ['RedisUtil']

Field = Union[int, float, str]


class RedisUtil:
    """Redis操作工具类"""
    prefix: str = get_settings().redis_prefix
    redis: Redis = redis_be.redis

    @staticmethod
    def get_key(key: str) -> str:
        """key通用前缀"""
        return f'{RedisUtil.prefix}{key}'

    @staticmethod
    async def info(section: Union[str, None] = None) -> dict:
        """Redis服务信息"""
        return await RedisUtil.redis.info(section)

    @staticmethod
    async def dbsize() -> dict:
        """当前数据库key数量"""
        return await RedisUtil.redis.dbsize()

    @classmethod
    async def set(cls, key: str, value: Field, time: int = None):
        """设置键值对"""
        await RedisUtil.redis.set(cls.get_key(key), value=value, ex=time)

    @classmethod
    async def get(cls, key: str) -> str:
        """获取key的值"""
        return await RedisUtil.redis.get(cls.get_key(key))

    @classmethod
    async def exists(cls, *keys: str) -> int:
        """判断多项key是否存在
            返回存在的key数量
        """
        return await RedisUtil.redis.exists(*(cls.get_key(key) for key in keys))

    @classmethod
    async def sset(cls, key: str, *values: Field) -> int:
        """将数据放入set缓存
            返回添加的数量
        """
        return await RedisUtil.redis.sadd(cls.get_key(key), *values)

    @classmethod
    async def sget(cls, key: str) -> Set:
        """根据key获取Set中的所有值"""
        return await RedisUtil.redis.smembers(cls.get_key(key))

    @classmethod
    async def hmset(cls, key: str, mapping: dict, time: int = None) -> int:
        """设置key, 通过字典的方式设置多个field, value对
            返回添加的数量
        """
        cnt = await RedisUtil.redis.hset(cls.get_key(key), mapping=mapping)
        if time and time > 0:
            await cls.expire(key, time)
        return cnt

    @classmethod
    async def hset(cls, key: str, field: str, value: Field, time: int = None) -> int:
        """向hash表中放入数据,如果不存在将创建
            返回添加的数量
        """
        return await cls.hmset(cls.get_key(key), mapping={field: value}, time=time)

    @classmethod
    async def hget(cls, key: str, field: str) -> str:
        """获取key中field域的值"""
        return await RedisUtil.redis.hget(cls.get_key(key), field)

    @classmethod
    async def hexists(cls, key: str, field: str) -> bool:
        """判断key中有没有field域名"""
        return await RedisUtil.redis.hexists(cls.get_key(key), field)

    @classmethod
    async def hdel(cls, key: str, *fields: str) -> int:
        """删除hash表中的值
            返回删除的数量
        """
        return await RedisUtil.redis.hdel(cls.get_key(key), *fields)

    @classmethod
    async def ttl(cls, key: str) -> int:
        """根据key获取过期时间"""
        return await RedisUtil.redis.ttl(cls.get_key(key))

    @classmethod
    async def expire(cls, key: str, time: int):
        """指定缓存失效时间"""
        await RedisUtil.redis.expire(cls.get_key(key), time)

    @classmethod
    async def delete(cls, *keys: str):
        """删除一个或多个键"""
        await RedisUtil.redis.delete(*(cls.get_key(key) for key in keys))
