# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field


class ChatGPTFormRequest(BaseModel):
    message: str = Field(default="", title="内容")