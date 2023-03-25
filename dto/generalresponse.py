# -*- coding: utf-8 -*-

from typing import Any
from pydantic import BaseModel, Field


class GeneralResponse(BaseModel):
    code: int = Field(default=0, title="状态码")
    msg: str = Field(default="ok", title="消息")
    data: Any = Field(default=None, title="数据")