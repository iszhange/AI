# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field


class ChatGPTFormRequest(BaseModel):
    uuid: str = Field(default="", title="UUID")
    message: str = Field(default="", title="内容")