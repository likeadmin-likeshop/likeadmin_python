from like.common.sms_captcha import SmsCaptchaManager
from like.config import get_settings
from like.plugins.notice.template.sms_template import SmsTemplate
from like.plugins.sms.sms_driver import SmsDriver
from like.utils.config import ConfigUtil
from like.utils.redis import RedisUtil


class SmsNotice(object):
    """
    短信通知
    """

    async def send(self, notice_params, sms_template: SmsTemplate):
        """
        发送短信通知
        :param notice_params:
        :return:
        """
        mobile = str(notice_params.get("mobile"))
        scene = notice_params.get("scene")
        params = notice_params.get("params")
        if mobile:
            template_params = await self.get_sms_params(params, sms_template.content)
            sms_content = self.get_content(params, sms_template.content)
            sms_driver = SmsDriver(scene=scene, mobile=mobile, template_id=sms_template.template_id,
                                   sms_content=sms_content, template_params=template_params)
            # await sms_driver.init()
            await sms_driver.send_sms()
            # 通知类型sms_type: [1=业务, 2=验证码]
            if sms_template.sms_type == 2 and params.get("code"):
                # 缓存验证码
                code = params["code"]
                await SmsCaptchaManager.set_code(mobile, scene, code)

    async def get_sms_params(self, params, content):
        """
        腾讯云参数处理
        :param params:
        :param content:
        :return:
        """
        engine = await ConfigUtil.get_val("sms", "default", "")
        if engine != "tencent":
            return params

        # todo getSmsParams

    def get_content(self, params, content):
        """
        获取短信内容，
        :param params:  {"code":123456}
        :param content:  短信模板： “您正在登录，验证码${code}，切勿将验证码泄露于他人，本条验证码有效期5分钟”
        :return:
        """
        for k, v in params.items():
            search_replace = "${" + k + "}"
            content = content.replace(search_replace, str(v))

        return content
