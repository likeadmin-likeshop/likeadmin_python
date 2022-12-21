from qiniu import Auth, put_data, put_file

from like.utils.config import ConfigUtil


class QiniuStorage(object):

    engine = 'qiniu'

    async def get_upload_token(self, **kwargs):
        """
        :param kwargs:
        :return:
        """

        self.config = await ConfigUtil.get_map("storage", 'qiniu')
        accessKey = self.config.get("accessKey", "")
        secretKey = self.config.get("secretKey", "")
        self.bucket = self.config.get("bucket", "")
        self.auth = Auth(accessKey, secretKey)
        return self.auth.upload_token(self.bucket, **kwargs)

    async def _upload(self, upload_func, target_path, **kwargs):
        token = await self.get_upload_token()
        result, resp = upload_func(token, target_path, **kwargs)
        return result

    def upload_data(self, target_path, data, **kwargs):
        """
        通过stream上传到七牛
        :param target_path:  目标路径，即文档参数key
        :param data:    stream
        :param kwargs:
        :return:
        """
        return self._upload(put_data, target_path, data=data, **kwargs)

    def upload_file(self, target_path, local_file, **kwargs):
        """
        上传文件到七牛
        :param target_path: 目标路径，即文档参数key
        :param local_file:  本地文件路径
        :param kwargs:
        :return:
        """
        return self._upload(put_file, target_path, file_path=local_file, **kwargs)
