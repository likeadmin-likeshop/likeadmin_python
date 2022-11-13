from abc import ABC, abstractmethod
from typing import List

from like.admin.schemas.setting import SettingCopyrightIn
from like.utils.config import ConfigUtil
from like.utils.tools import ToolsUtil


class ISettingCopyrightService(ABC):
    """网站备案服务抽象类"""

    @abstractmethod
    async def detail(self) -> List[dict]:
        pass

    @abstractmethod
    async def save(self, copyright_in: SettingCopyrightIn):
        pass


class SettingCopyrightService(ISettingCopyrightService):
    """网站备案服务实现类"""

    async def detail(self) -> List[dict]:
        """获取网站备案信息"""
        config = await ConfigUtil.get_val('website', 'copyright', '[]')
        return ToolsUtil.json_to_map(config)

    async def save(self, copyright_in: SettingCopyrightIn):
        """保存网站备案信息"""
        await ConfigUtil.set('website', 'copyright', copyright_in.json(ensure_ascii=False))

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
