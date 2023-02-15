from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects import mysql

from like.models.base import Base

__all__ = [
    'decorate_page',
    'decorate_tabbar',
    'DecoratePage',
    'DecorateTabbar'
]


class DecoratePage(Base):
    """
    页面装修表
    """
    __tablename__ = 'la_decorate_page'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '页面装修表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')

    page_type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('10'), comment='页面类型')
    page_name = Column(String(100), nullable=False, server_default='', comment='页面名称')
    page_data = Column(Text, server_default='', comment='页面数据')

    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')


class DecorateTabbar(Base):
    """
    底部装修表
    """
    __tablename__ = 'la_decorate_tabbar'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '底部装修表',
    }
    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    name = Column(String(20), nullable=False, server_default='', comment='导航名称')
    selected = Column(String(200), nullable=False, server_default='', comment='已选图标')
    unselected = Column(String(200), nullable=False, server_default='', comment='未选图标')
    link = Column(String(200), nullable=False, server_default='', comment='链接地址')
    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')


decorate_page = DecoratePage.__table__
decorate_tabbar = DecorateTabbar.__table__
