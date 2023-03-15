import time
from abc import ABC, abstractmethod

from sqlalchemy import select

from like.dependencies.database import db
from like.exceptions.base import AppException
from like.front.schemas.sms import SmsSendIn
from like.http_base import HttpResp
from like.models.system import system_log_sms
from like.plugins.notice.notice_driver import NoticeDriver
from like.utils.tools import ToolsUtil


class ISmsSendService(ABC):

    @abstractmethod
    def send(self, send_params: SmsSendIn):
        """
        发送验证码
        :param send_params:
        :return:
        """
        pass


class SmsSendService(ISmsSendService):

    async def send(self, send_params: SmsSendIn):
        """
        发送验证码
        :param send_params:
        :return:
        """

        sms_log = await db.fetch_one(
            select([system_log_sms.c.id, system_log_sms.c.create_time]).select_from(system_log_sms).where(
                system_log_sms.c.mobile == send_params.mobile,
                system_log_sms.c.scene == send_params.scene,
                system_log_sms.c.status.in_({0, 1})
            ).order_by(system_log_sms.c.id.desc()).limit(1))

        if sms_log and sms_log.create_time <= int(time.time() / 1000 - 60):
            raise AppException(HttpResp.FAILED, msg='操作频繁,请稍后再试!!')

        sms_params = {"scene": send_params.scene, "mobile": send_params.mobile,
                      "params": {"code": ToolsUtil.random_int(4)}}

        await NoticeDriver().handle(sms_params)

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
