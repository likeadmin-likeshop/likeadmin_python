from like.app import create_front

# 容器运行入口
app = create_front()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8002)
