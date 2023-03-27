import copy
import json
from abc import ABC, abstractmethod

from like.admin.schemas.setting import SettingSmsSaveIn
from like.utils.config import ConfigUtil


class ISettingSmsService(ABC):
    """短信配置服务抽象类"""

    @abstractmethod
    async def list(self) -> list:
        pass

    @abstractmethod
    async def detail(self, alias: str) -> dict:
        pass

    @abstractmethod
    async def save(self, save_in: SettingSmsSaveIn):
        pass


class SettingSmsService(ISettingSmsService):
    """短信配置服务实现类"""
    engines = {
        'aliyun': {'name': '阿里云短信', 'alias': 'aliyun'},
        'tencent': {'name': '腾讯云短信', 'alias': 'tencent'},
    }

    async def list(self) -> list:
        """短信引擎列表"""
        engine = await ConfigUtil.get_val('sms', 'default', 'aliyun')
        res = []
        for k, v in copy.deepcopy(self.engines).items():
            status = 0
            if k == engine:
                status = 1
            v['status'] = status
            res.append(v)
        return res

    async def detail(self, alias: str) -> dict:
        """短信引擎详情"""
        engine = await ConfigUtil.get_val('sms', 'default', 'local')
        config = await ConfigUtil.get_map('sms', alias)
        res = {'name': config.get('name', ''),
               'status': 1 if engine == alias else 0, 'alias': alias,
               'sign': config.get('sign', '')}
        if alias == 'aliyun':
            res['appKey'] = config.get('appKey', '')
            res['secretKey'] = config.get('secretKey', '')
        elif alias == 'tencent':
            res['appId'] = config.get('appId', '')
            res['secretId'] = config.get('secretId', '')
            res['secretKey'] = config.get('secretKey', '')
        elif alias == 'huawei':
            pass
        return res

    async def save(self, save_in: SettingSmsSaveIn):
        """短信引擎保存"""
        await ConfigUtil.set('sms', save_in.alias, json.dumps(save_in.dict(exclude_none=True), ensure_ascii=False))
        engine = await ConfigUtil.get_val('sms', 'default', '')
        if save_in.status == 1:
            await ConfigUtil.set('sms', 'default', save_in.alias)
        elif engine == save_in.alias and save_in.status == 0:
            await ConfigUtil.set('sms', 'default', '')

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
