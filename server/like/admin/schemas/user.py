from typing import Union

from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    description: Union[str, None] = None


class UserOut(BaseModel):
    name: str
