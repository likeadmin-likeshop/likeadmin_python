from tencentcloud.common import credential
# 导入可选配置类
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
# 导入对应产品模块的client models。
from tencentcloud.sms.v20210111 import sms_client, models

from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.plugins.sms.engine.sms_base import SmsBase


class TencentSms(SmsBase):
    engine = 'tencent'

    def __init__(self, **kwargs):
        self.status = 0
        super(TencentSms, self).__init__(**kwargs)

    def get_status(self):
        """
        发送状态：[0=发送中, 1=发送成功, 2=发送失败]
        :return:
        """
        return self.status

    @staticmethod
    def get_client(config):
        secret_id = config.get("secretId")
        secret_key = config.get("secretKey")
        cred = credential.Credential(secret_id, secret_key)

        # 实例化一个http选项，可选的，没有特殊需求可以跳过。
        httpProfile = HttpProfile()
        # 如果需要指定proxy访问接口，可以按照如下方式初始化hp
        # httpProfile = HttpProfile(proxy="http://用户名:密码@代理IP:代理端口")
        httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
        httpProfile.reqTimeout = 60  # 请求超时时间，单位为秒(默认60秒)
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

        clientProfile = ClientProfile()
        clientProfile.signMethod = "HmacSHA256"  # 指定签名算法
        clientProfile.httpProfile = httpProfile

        return sms_client.SmsClient(cred, "ap-beijing", clientProfile)

    def send(self, mobile, config, template_id, template_params):
        """
        发送短信
        :param mobile:
        :param config:
        :param template_id:
        :param template_params:
        :return:
        """
        sms_client = self.get_client(config)
        req = models.SendSmsRequest()
        req.SmsSdkAppId = config.get("appId")
        req.SignName = config.get("sign")
        req.TemplateId = template_id
        req.PhoneNumberSet = ["+86{}".format(mobile.strip()), ]
        req.TemplateParamSet = template_params

        response = sms_client.SendSms(req)

        try:
            resp_data = response.SendStatusSet[0]

            if resp_data.Code.upper() != "OK":
                self.status = 2
                return resp_data.Message
            self.status = 1
            return response
        except Exception as e:
            self.status = 2
            raise AppException(HttpResp.FAILED, echo_exc=True, msg=str(e))
