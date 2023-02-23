from like.config import get_settings
from like.utils.redis import RedisUtil


class SmsCaptchaManager(object):

    @staticmethod
    def get_key(mobile, scene):
        return r"{get_settings().redisSmsCode}{scene}:{mobile}"

    @classmethod
    async def set_code(cls, mobile, scene, code):
        sms_key = cls.get_key(mobile, scene)
        return await RedisUtil.set(sms_key, code, 900)

    @classmethod
    async def get_code(cls, mobile, scene):
        sms_key = cls.get_key(mobile, scene)
        return await RedisUtil.get(sms_key)

    @classmethod
    async def del_code(cls,mobile, scene):
        sms_key = cls.get_key(mobile, scene)
        return await RedisUtil.delete(sms_key)
