# -*- coding: utf8 -*-
"""
AI Workstation
author: ken
date: 2023-03-22
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import openai


description = """
AI Workstation 是AI工具集合
"""

tags_metadata = [
    # {
    #     "name": "openai",
    #     "description": "OpenAI API接口接入"
    # }
]

app = FastAPI(
    title="AI Workstition",
    description=description,
    version="0.0.1",
    terms_of_service="http://localhost:5959",
    contact={
        "name": "ken zhang",
        "url": "https://github.com/iszhange",
        "email": "kenphp@yeah.net"
    },
    license_info={},
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    openai.router,
    prefix="/openai",
    tags=["OpenAI"]
)

@app.get("/")
async def index():
    return {"message": "Welcome AI Workstation!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5959)
