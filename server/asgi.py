from like.app import create_app
import uvicorn

# 容器运行入口
app = create_app()
uvicorn.run(app, host='0.0.0.0', port=8000)
