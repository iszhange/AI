# -*- coding: utf-8 -*-
"""
ChatGPT
author: ken zhang
date: 2023.03.25
"""
import openai
from dto.openai import chatgptmodel
from config.openai import api_key


class ChatGPT(object):

    def chat(self, request: chatgptmodel.ChatGPTFormRequest):
        openai.api_key = api_key
        return openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": request.message}])
