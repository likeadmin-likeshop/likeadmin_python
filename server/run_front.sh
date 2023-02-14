#!/usr/bin/env bash

# 运行服务
python3 -m uvicorn asgi-front:app --port 8002 --reload
