from functools import lru_cache

from pydantic import BaseSettings as Base


__all__ = ['get_settings']


class BaseSettings(Base):
    class Config:
        env_file = '.env', '.env.prod'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    """应用配置"""
    # 系统加密字符
    secret: str = 'UVTIyzCy'
    # 数据源配置
    database_url: str = 'mysql+pymysql://root:root@localhost:3306/likeadmin?charset=utf8mb4'
    database_pool_min_size: int = 5
    database_pool_max_size: int = 20
    # 上传文件路径
    upload_directory: str = '/tmp/uploads/likeadmin-python/'
    # Redis源配置
    redis_url: str = 'redis://localhost:6379'
    # Redis键前缀
    redis_prefix: str = 'Like:'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
