# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.utils.config import ConfigUtil


class QCloudStorage(object):
    engine = 'qiniu'

    async def get_client(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        try:
            self.config = await ConfigUtil.get_map("storage", 'qcloud')
            self.bucket = self.config.get("bucket", "")
            secret_id = self.config.get("accessKey", "")
            secret_key = self.config.get("secretKey", "")
            region = self.config.get("region", "")
            config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
            return CosS3Client(config)
        except Exception as e:
            raise AppException(HttpResp.FAILED, msg=str(e))

    async def upload_data(self, target_path, data, **kwargs):
        """
        通过stream上传到七牛
        :param target_path:  目标路径，即文档参数key
        :param data:    stream
        :param kwargs:
        :return:
        """
        client = await self.get_client()
        try:
            response = client.put_object(Bucket=self.bucket, Body=data, Key=target_path)
            if response['ETag']:
                return target_path
        except Exception as e:
            raise AppException(HttpResp.FAILED, msg=str(e))
        return ''
