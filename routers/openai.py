# -*- coding: utf-8 -*-
"""
OpenAI路由
author: ken
date: 2023-03-25
"""

from fastapi import APIRouter
from dto.openai import chatgptmodel
from dto import generalresponse
from typing import Any
from internal.openai import chatgpt


router = APIRouter()


@router.post("/chat", response_model=generalresponse.GeneralResponse)
async def chat(body: chatgptmodel.ChatGPTFormRequest) -> Any:
    m = chatgpt.ChatGPT()

    response = generalresponse.GeneralResponse()
    response.code = 200
    response.msg = "ok"
    response.data = await m.chat(body)

    return response
