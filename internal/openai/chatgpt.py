# -*- coding: utf-8 -*-
"""
ChatGPT
author: ken zhang
date: 2023.03.25
"""
import openai
import uuid
import datetime
import hashlib
import asyncio
from configparser import ConfigParser
from dto.openai import chatgptmodel
from library import mariadb


class ChatGPT(object):

    def __init__(self):
        self.model = "gpt-3.5-turbo"

        self.config = ConfigParser()
        self.config.read("config.ini")

    async def chat(self, request: chatgptmodel.ChatGPTFormRequest):
        # 组合消息体
        messages = []
        if request.uuid == "":
            # 新会话的话生成唯一uuid
            request.uuid = self.generate_uuid(request.message)
        else:
            # 获取历史消息
            messages = self.get_history_conversation_messages(request.uuid)
        messages.append({"role": "user", "content": request.message})
        
        # 请求openai
        openai.api_key = self.config.get("openai", "api_key")
        response = openai.ChatCompletion.create(model=self.model, messages=messages)

        # 保存会话数据
        asyncio.create_task(self.save_conversation(request.uuid, request.message, response["choices"][0]["message"]["content"]))
        
        return {"uuid": request.uuid, "message": response}

    async def save_conversation(self, custom_uuid:str, user_content:str, assistant_content:str):
        """
        保存会话数据
        :param custom_uuid: UUID
        :param user_content: 问题
        :param assistant_content: 回答
        """
        with mariadb.MariaDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(("SELECT id FROM chatgpt_conversations WHERE uuid=%s LIMIT 1"), (custom_uuid,))
            result = cursor.fetchone()
            date_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if result is None:
                data = {
                    "uuid": custom_uuid,
                    "updated_at": date_at,
                    "created_at": date_at,
                }
                cursor.execute(("INSERT INTO chatgpt_conversations (uuid,updated_at,created_at) VALUES(%(uuid)s, %(updated_at)s, %(created_at)s)"), data)
                conversation_id = cursor.lastrowid
            else:
                conversation_id = result[0]
            
            data = [{
                "conversation_id": conversation_id,
                "role": "user",
                "content": user_content,
                "updated_at": date_at,
                "created_at": date_at,
            },{
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": assistant_content,
                "updated_at": date_at,
                "created_at": date_at,
            }]
            cursor.executemany(("INSERT INTO chatgpt_conversation_messages (conversation_id,role,content,updated_at,created_at) VALUES(%(conversation_id)s, %(role)s, %(content)s, %(updated_at)s, %(created_at)s)"), data)
            cnx.commit()
            cursor.close()
        
    def get_history_conversation_messages(self, custom_uuid: str):
        """
        获取历史会话消息
        :custom_uuid (str): UUID
        :return: list
        """
        messages = []
        with mariadb.MariaDB() as cnx:
            cursor = cnx.cursor()
            cursor.execute(("SELECT a.role,a.content FROM chatgpt_conversation_messages AS a LEFT JOIN chatgpt_conversations AS b ON a.conversation_id=b.id WHERE b.uuid=%s AND b.is_del=0 ORDER BY a.id ASC"), (custom_uuid,))
            for (role, content) in cursor:
                messages.append({"role": role, "content": content})
            cursor.close()
        
        return messages

    def generate_uuid(self, user_content: str):
        """
        生成uuid
        :user_content: str
        :return: str
        """
        hasher = hashlib.sha256()
        hasher.update(user_content)
        digest = hasher.hexdigest()
        serial_number = digest[:10]
        namespace_uuid = uuid.uuid4()
        custom_uuid = uuid.uuid5(namespace_uuid, serial_number)

        return str(custom_uuid)

