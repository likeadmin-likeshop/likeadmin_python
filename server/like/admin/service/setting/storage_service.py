"""
存储设置
"""
import json
from abc import ABC, abstractmethod

import pydantic

from like.admin.schemas.setting import SettingsStorageEditIn, SettingsStorageDetailOut, SettingsStorageOut
from like.utils.config import ConfigUtil

SettingsStorageConfDict = {
    'local': {"name": "本地存储", "describe": "存储在本地服务器"},
    'qiniu': {"name": "七牛云存储", "describe": "存储在七牛云，请前往七牛云开通存储服务"},
    'aliyun': {"name": "阿里云存储", "describe": "存储在阿里云，请前往阿里云开通存储服务"},
    'qcloud': {"name": "腾讯云存储", "describe": "存储在腾讯云，请前往腾讯云开通存储服务"}
}


class ISettingStorageService(ABC):
    """存储配置服务接口类"""

    @abstractmethod
    async def list(self):
        pass

    @abstractmethod
    async def detail(self, alias: str):
        pass

    @abstractmethod
    async def edit(self, params: SettingsStorageEditIn):
        pass

    @abstractmethod
    async def change(self, alias: str, status: int):
        pass


class SettingStorageService(ISettingStorageService):
    """存储配置服务实现"""

    async def list(self):
        engine = await ConfigUtil.get_val("storage", "default", "local")
        return [SettingsStorageOut(
            **{"alias": alias, "name": conf['name'], "describe": conf['describe'], 'status': int(engine == alias)}) for
            alias, conf in SettingsStorageConfDict.items()]

    async def detail(self, alias: str):
        engine = await ConfigUtil.get_val("storage", "default", "local")
        config = await ConfigUtil.get_map("storage", alias) or {}
        detail = {
            "name": config.get("name", ""),
            "alias": alias,
            "status": engine == alias
        }
        if alias != 'local':
            detail.update({
                "bucket": config.get("bucket", ""),
                "secretKey": config.get("secretKey", ""),
                "accessKey": config.get("accessKey", ""),
                "domain": config.get("domain", ""),
            })
            if alias == "qcloud":
                detail.update({
                    "region": config.get("region")
                })
        return pydantic.parse_obj_as(SettingsStorageDetailOut, detail)

    async def edit(self, params: SettingsStorageEditIn):
        alias = params.alias
        status = params.status
        assert alias, 'alias参数缺失'
        assert alias in SettingsStorageConfDict, '暂不支持该存储方式'
        assert status is not None, 'status参数缺失'
        if alias == 'local':
            conf = {
                "name": "本地存储",
            }
        else:
            conf = {
                "bucket": params.bucket,
                "secretKey": params.secretKey,
                "accessKey": params.accessKey,
                "domain": params.domain,
            }
        await ConfigUtil.set("storage", alias, json.dumps(conf))
        engine = await ConfigUtil.get_val("storage", "default", "local")
        if status:
            await ConfigUtil.set("storage", "default", alias)
        elif engine == alias and not status:
            await ConfigUtil.set("storage", "default", "")

    async def change(self, alias: str, status: int):
        engine = await ConfigUtil.get_val("storage", "default", "local")
        if engine == alias and status == 0:
            await ConfigUtil.set("storage", "default", "")
        else:
            await ConfigUtil.set("storage", "default", alias)

    @classmethod
    async def instance(cls):
        return cls()
