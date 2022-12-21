import oss2

from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.utils.config import ConfigUtil


class AliyunStorage(object):
    engine = 'aliyun'

    @staticmethod
    async def oss_client(**kwargs):
        """
        :param kwargs:
        :return:
        """
        config = await ConfigUtil.get_map("storage", 'aliyun')
        access_key = config.get("accessKey", "")
        secret_key = config.get("secretKey", "")
        bucket_name = config.get("bucket", "")
        endpoint = "https://oss-cn-hangzhou.aliyuncs.com"
        auth = oss2.Auth(access_key, secret_key)
        return oss2.Bucket(auth, endpoint, bucket_name)

    @classmethod
    async def upload_data(cls, target_path, data, **kwargs):
        """
        通过stream上传阿里云
        :param target_path:  目标路径，即文档参数key
        :param data:    stream
        :param kwargs:
        :return:
        """
        try:
            bucket = await cls.oss_client()
            resp = bucket.put_object(target_path, data)
            return resp.resp.response.url
        except oss2.exceptions.OssError as e:
            raise AppException(HttpResp.SYSTEM_ERROR, msg='上传文件失败:%s' % e.message)