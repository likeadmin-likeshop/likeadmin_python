from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects import mysql

from .base import Base

__all__ = [
    'OfficialReply', 'official_reply'
]


class OfficialReply(Base):
    """公众号回复实体"""
    __tablename__ = 'la_official_reply'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '公众号的回复表',
    }

    id = Column(mysql.INTEGER(11, unsigned=True), primary_key=True, comment='主键')
    name = Column(String(64), nullable=False, server_default='', comment='规则名')
    keyword = Column(String(64), nullable=False, server_default='', comment='关键词')
    reply_type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                        comment='回复类型: [1=关注回复 2=关键字回复, 3=默认回复]')
    matching_type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                           comment='匹配方式: [1=全匹配, 2=模糊匹配]')
    content_type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                          comment='内容类型: [1=文本]')
    status = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                    comment='启动状态: [1=启动, 0=关闭]')
    content = Column(Text, nullable=False, comment='回复内容')
    sort = Column(mysql.INTEGER(11, unsigned=True), nullable=False, server_default=text('50'), comment='排序编号')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否删除: [0=否, 1=是]')
    create_time = Column(mysql.INTEGER(10, unsigned=True), server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), server_default=text('0'), comment='更新时间')
    delete_time = Column(mysql.INTEGER(10, unsigned=True), server_default=text('0'), comment='删除时间')


official_reply = OfficialReply.__table__
