import time
from abc import ABC, abstractmethod
from typing import Final, List

from fastapi import Depends

from like.admin.config import AdminConfig
from like.admin.schemas.system import (
    SystemAuthMenuCreateIn, SystemAuthMenuEditIn, SystemAuthMenuOut)
from like.dependencies.database import db
from like.models import system_auth_menu
from like.utils.redis import RedisUtil
from .auth_perm import ISystemAuthPermService, SystemAuthPermService


class ISystemAuthMenuService(ABC):
    """系统菜单服务抽象类"""

    @abstractmethod
    async def select_menu_by_role_id(self, role_id) -> List[SystemAuthMenuOut]:
        pass

    @abstractmethod
    async def list(self) -> List[SystemAuthMenuOut]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> SystemAuthMenuOut:
        pass

    @abstractmethod
    async def add(self, create_in: SystemAuthMenuCreateIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: SystemAuthMenuEditIn):
        pass

    @abstractmethod
    async def delete(self, id_: int):
        pass


class SystemAuthMenuService(ISystemAuthMenuService):
    """系统菜单服务实现类"""

    async def select_menu_by_role_id(self) -> List[SystemAuthMenuOut]:
        pass

    async def list(self) -> List[SystemAuthMenuOut]:
        pass

    async def detail(self, id_: int) -> SystemAuthMenuOut:
        pass

    async def add(self, create_in: SystemAuthMenuCreateIn):
        pass

    async def edit(self, edit_in: SystemAuthMenuEditIn):
        pass

    async def delete(self, id_: int):
        pass

    def __init__(self, auth_perm_service: ISystemAuthPermService):
        self.auth_perm_service: Final[ISystemAuthPermService] = auth_perm_service

    @classmethod
    async def instance(cls, auth_perm_service: ISystemAuthPermService = Depends(SystemAuthPermService.instance)):
        """实例化"""
        return cls(auth_perm_service)
