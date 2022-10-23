from pydantic import BaseModel


class SystemLoginIn(BaseModel):
    """系统登录参数"""
    username: str
    password: str


class SystemLoginOut(BaseModel):
    """系统登录返回信息"""
    token: str


class SystemLogoutIn(BaseModel):
    """退出登录参数"""
    token: str
