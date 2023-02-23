
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.plugins.sms.engine.sms_base import SmsBase


class AliyunSms(SmsBase):
    engine = 'aliyun'

    def __init__(self, **kwargs):
        self.status = 0
        super(AliyunSms, self).__init__(**kwargs)

    def get_status(self):
        """
        发送状态：[0=发送中, 1=发送成功, 2=发送失败]
        :return:
        """
        return self.status

    @staticmethod
    def get_client(config):
        app_key = config.get("appKey")
        secret_key = config.get("secretKey")
        return AcsClient(app_key, secret_key)

    def send(self, mobile, config, template_id, template_params):
        """
        发送短信
        :param mobile:
        :param config:
        :param template_id:
        :param template_params:
        :return:
        """
        request = CommonRequest(domain="dysmsapi.aliyuncs.com", version="2017-05-25", action_name="SendSms")
        request.set_method("POST")
        request.set_protocol_type("https")
        request.add_query_param("PhoneNumbers", mobile)
        request.add_query_param("SignName", config.get("sign"))
        request.add_query_param("TemplateCode", template_id)
        request.add_query_param("TemplateParam", template_params)
        client = self.get_client(config)
        response = client.do_action_with_exception(request)
        try:
            resp_data = json.loads(response)
            if resp_data.get("Code") != "OK" or resp_data.get("Message") != "OK":
                self.status = 2
                return resp_data.get("Message")
            self.status = 1
            return response
        except Exception as e:
            self.status = 2
            raise AppException(HttpResp.FAILED, echo_exc=True, msg=str(e))