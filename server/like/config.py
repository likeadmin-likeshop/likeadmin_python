from functools import lru_cache

from pydantic import BaseSettings as Base


__all__ = ['get_settings']


class BaseSettings(Base):
    class Config:
        env_file = '.env', '.env.prod'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    """应用配置"""
    # 数据源配置
    database_url: str = 'mysql+pymysql://root:root@localhost:3306/likeadmin?charset=utf8mb4'
    # 上传文件路径
    upload_directory: str = '/tmp/uploads/likeadmin-python/'
    # Redis源配置
    redis_url: str = 'redis://localhost:6379'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
