from fastapi import Query
from pydantic import BaseModel


class SmsSendIn(BaseModel):
    """
    短信发送 入参
    """
    scene: int  # 场景  [101=登录验证码, 102=绑定手机验证码, 103=变更手机验证码, 104=找回登录密码验证码]
    mobile: str = Query(max_length=11, min_length=11, regex="^[1][3,4,5,6,7,8,9][0-9]{9}$")
