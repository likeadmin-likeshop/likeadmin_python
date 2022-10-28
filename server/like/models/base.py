from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER

__all__ = ['Base', 'TimestampMixin']

# 数据库模型基类
Base = declarative_base()


class TimestampMixin:
    create_time = Column(INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')
    delete_time = Column(INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='删除时间')
