from functools import lru_cache

from pydantic import BaseSettings as Base

__all__ = ['get_settings']


class BaseSettings(Base):
    """配置基类"""

    class Config:
        env_file = '.env', '.env.prod'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    """应用配置
        server目录为后端项目根目录, 在该目录下创建 ".env" 文件, 写入环境变量(默认大写)会自动加载, 并覆盖同名配置(小写)
            eg.
            .env 文件内写入:
                UPLOAD_DIRECTORY='/tmp/test/'
                REDIS_URL='redis://localhost:6379'

                上述环境变量会覆盖 upload_directory 和 redis_url
    """
    # 上传文件路径
    upload_directory: str = '/tmp/uploads/likeadmin-python/'

    # 数据源配置
    database_url: str = 'mysql+pymysql://root:root@localhost:3306/likeadmin?charset=utf8mb4'
    # 数据库连接池最小值
    database_pool_min_size: int = 5
    # 数据库连接池最大值
    database_pool_max_size: int = 20

    # Redis源配置
    redis_url: str = 'redis://localhost:6379'
    
    # 全局配置
    # 系统加密字符
    secret: str = 'UVTIyzCy'
    # Redis键前缀
    redis_prefix: str = 'Like:'


@lru_cache()
def get_settings() -> Settings:
    """获取并缓存应用配置"""
    return Settings()
