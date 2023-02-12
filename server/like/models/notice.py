from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects import mysql

from .base import Base, TimestampMixin

__all__ = [
    'NoticeSetting', 'notice_setting',
]


class NoticeSetting(Base, TimestampMixin):
    """通知设置实体"""
    __tablename__ = 'la_notice_setting'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '消息通知设置表',
    }

    id = Column(mysql.INTEGER(11, unsigned=True), primary_key=True, comment='主键')
    scene = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='场景编号')
    name = Column(String(100), nullable=False, server_default='', comment='场景名称')
    remarks = Column(String(200), nullable=False, server_default='', comment='场景描述')
    recipient = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='接收人员: [1=用户, 2=平台]')
    type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                  comment='通知类型: [1=业务, 2=验证]')
    system_notice = Column(Text, nullable=True, comment='系统的通知设置')
    sms_notice = Column(Text, nullable=True, comment='短信的通知设置')
    oa_notice = Column(Text, nullable=True, comment='公众号通知设置')
    mnp_notice = Column(Text, nullable=True, comment='小程序通知设置')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否删除: [0=否, 1=是]')


notice_setting = NoticeSetting.__table__
