from fastapi import Query
from pydantic import BaseModel

from like.front.config import LoginClientEnum, LoginTypeEnum


class FrontLoginCheckOut(BaseModel):
    """
    登录管理 返回信息
    """
    id: int
    token: str
    isBindMobile: bool


class FrontRegisterIn(BaseModel):
    """
    注册 入参
    """
    username: str = Query(min_length=3, max_length=12, regex='^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{3,12}$')
    password: str = Query(min_length=6, max_length=12)
    client: LoginClientEnum


class FrontLoginCheckIn(BaseModel):
    """
    手机端-登录管理 入参
    """
    scene: LoginTypeEnum  # 登录方式
    client: LoginClientEnum  # 登录端
    username: str = Query(default=None)
    mobile: str = Query(default=None)
    password: str = Query(default=None)
    code: str = Query(default=None)
