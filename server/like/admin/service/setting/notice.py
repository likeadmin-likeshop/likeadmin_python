import json
import time
from abc import ABC, abstractmethod

from like.admin.schemas.setting import SettingNoticeListOut, SettingNoticeDetailOut, SettingNoticeSaveIn
from like.dependencies.database import db
from like.models import notice_setting


class ISettingNoticeService(ABC):
    """通知设置服务抽象类"""

    @abstractmethod
    async def list(self, recipient: int) -> list:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> SettingNoticeDetailOut:
        pass

    @abstractmethod
    async def save(self, save_in: SettingNoticeSaveIn):
        pass


class SettingNoticeService(ISettingNoticeService):
    """通知设置服务实现类"""
    engines = {
        'aliyun': {'name': '阿里云短信', 'alias': 'aliyun'},
        'tencent': {'name': '腾讯云短信', 'alias': 'tencent'},
    }

    async def list(self, recipient: int) -> list:
        """通知设置列表"""
        settings = await db.fetch_all(
            notice_setting.select()
            .where(notice_setting.c.recipient == recipient, notice_setting.c.is_delete == 0)
            .order_by(notice_setting.c.id))
        res = []
        for s in settings:
            o = dict(s)
            if s.type == 1:
                o['type'] = '业务通知'
            else:
                o['type'] = '验证码'
            system_dict = json.loads(s.system_notice)
            sms_dict = json.loads(s.sms_notice)
            oa_dict = json.loads(s.oa_notice)
            mnp_dict = json.loads(s.mnp_notice)
            o['system_status'] = system_dict.get('status', 0)
            o['sms_status'] = sms_dict.get('status', 0)
            o['oa_status'] = oa_dict.get('status', 0)
            o['mnp_status'] = mnp_dict.get('status', 0)
            res.append(SettingNoticeListOut(**o))
        return res

    async def detail(self, id_: int) -> SettingNoticeDetailOut:
        """通知设置详情"""
        setting = await db.fetch_one(
            notice_setting.select()
            .where(notice_setting.c.id == id_, notice_setting.c.is_delete == 0).limit(1))
        assert setting
        system_dict = json.loads(setting.system_notice)
        sms_dict = json.loads(setting.sms_notice)
        oa_dict = json.loads(setting.oa_notice)
        mnp_dict = json.loads(setting.mnp_notice)
        setting_dict = dict(setting)
        setting_dict['system_notice'] = system_dict
        setting_dict['sms_notice'] = sms_dict
        setting_dict['oa_notice'] = oa_dict
        setting_dict['mnp_notice'] = mnp_dict
        setting_dict['type'] = '业务通知' if setting_dict['type'] == 1 else '验证码'
        return SettingNoticeDetailOut(**setting_dict)

    async def save(self, save_in: SettingNoticeSaveIn):
        """通知设置保存"""
        setting = await db.fetch_one(
            notice_setting.select()
            .where(notice_setting.c.id == save_in.id, notice_setting.c.is_delete == 0).limit(1))
        assert setting
        save_dict = save_in.dict(exclude_none=True)
        save_dict['system_notice'] = json.dumps(save_dict['system_notice'], ensure_ascii=False)
        save_dict['sms_notice'] = json.dumps(save_dict['sms_notice'], ensure_ascii=False)
        save_dict['oa_notice'] = json.dumps(save_dict['oa_notice'], ensure_ascii=False)
        save_dict['mnp_notice'] = json.dumps(save_dict['mnp_notice'], ensure_ascii=False)
        save_dict['update_time'] = int(time.time())
        await db.execute(notice_setting.update()
                         .where(notice_setting.c.id == save_in.id)
                         .values(**save_dict))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
