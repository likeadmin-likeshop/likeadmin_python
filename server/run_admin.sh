#!/usr/bin/env bash

# 运行服务
python3 -m uvicorn asgi:app --port 8000 --reload
