from abc import ABC, abstractmethod


class ISystemAuthDeptService(ABC):

    async def fetch_all_dept(self):
        pass

class SystemAuthDeptService():
    pass