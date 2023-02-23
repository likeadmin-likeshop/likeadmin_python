from sqlalchemy import select

from like.dependencies.database import db
from like.models.notice import notice_setting
from like.plugins.notice.engine.sms_notice import SmsNotice
from like.plugins.notice.template.sms_template import SmsTemplate


class NoticeDriver(object):
    async def handle(self, notice_params:dict):
        """
        notice_params:   {
                            "scene": send_params.scene,
                            "mobile": send_params.mobile,
                            "params":  {"code": ToolsUtil.random_int(4)}
                        }
        :param notice_params:
        :return:
        """
        scene = notice_params.get("scene")
        # 获取场景模板
        notice = await db.fetch_one(
            select([notice_setting.c.id, notice_setting.c.type, notice_setting.c.sms_notice]).select_from(
                notice_setting).where(
                notice_setting.c.scene == scene, notice_setting.c.is_delete == 0).order_by(
                notice_setting.c.id.desc()).limit(1))
        assert notice, "消息场景不存在!"

        sms_template = SmsTemplate(notice.type, notice.sms_notice)

        if sms_template.status and sms_template.status == 1:
            await SmsNotice().send(notice_params, sms_template)
