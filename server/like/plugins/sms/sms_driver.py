import time

from like.dependencies.database import db
from like.models import system_log_sms
from like.plugins.sms.engine.sms_base import SmsBase
from like.utils.config import ConfigUtil


class SmsDriver():
    """
    短信发送驱动方法
    """

    def __init__(self, scene, mobile, template_id, sms_content='', template_params=None):
        self.mobile = mobile
        self.scene = scene
        self.template_id = template_id
        self.template_params = template_params
        self.sms_content = sms_content

    async def send_sms(self):
        """
        发送短信
        :return:
        """
        self.engine = await ConfigUtil.get_val("sms", "default", "")
        self.config = await ConfigUtil.get_map("sms", self.engine)
        log_id = await self.write_log()
        sms_instance = SmsBase.getInstance(self.engine)
        results = sms_instance.send(self.mobile, self.config, self.template_id, self.template_params)
        status = sms_instance.get_status()

        await self.update_log(log_id, status, results)
        return results

    async def write_log(self):
        """
        写入短信日志
        :return:
        """
        log_dict = {
            "mobile": self.mobile,
            "content": self.sms_content,
            "status": 0,
            "update_time": int(time.time()),
            "create_time": int(time.time())
        }
        return await db.execute(system_log_sms.insert().values(**log_dict))

    async def update_log(self, _id, status, result):
        """
        更新短信日志
        :param _id:
        :param status:
        :param result:
        :return:
        """
        log_update = {
            "scene": self.scene,
            "mobile": self.mobile,
            "status": status,
            "results": result,
            "send_time": int(time.time()),
            "update_time": int(time.time())

        }
        return await db.execute(system_log_sms.update()
                                .where(system_log_sms.c.id == _id)
                                .values(**log_update))
