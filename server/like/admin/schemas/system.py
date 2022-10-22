from pydantic import BaseModel


class SystemLoginIn(BaseModel):
    username: str
    password: str


class SystemLoginOut(BaseModel):
    token: str


class SystemLogoutIn(BaseModel):
    token: str
