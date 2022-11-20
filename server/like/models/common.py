from sqlalchemy import Column, String, text
from sqlalchemy.dialects import mysql

from .base import Base, TimestampMixin

__all__ = [
    'Album', 'common_album', 'common_album_cate', 'AlbumCate'
]


class Album(Base, TimestampMixin):
    """用户实体"""
    __tablename__ = 'la_album'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '相册管理表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键ID')
    cid = Column(mysql.INTEGER(10, unsigned=True), nullable=False, comment='类目ID')
    aid = Column(mysql.INTEGER(10, unsigned=True), nullable=False, comment='管理员ID')
    uid = Column(mysql.INTEGER(10, unsigned=True), nullable=False, comment='用户ID')

    type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('10'),
                  comment='文件类型: 10=图片,  20=视频')

    name = Column(String(100), nullable=False, server_default='', comment='文件名称')
    uri = Column(String(200), nullable=False, server_default='', comment='文件路径')
    ext = Column(String(10), nullable=False, server_default='', comment='文件扩展')

    size = Column(mysql.INTEGER(10, unsigned=True), nullable=False, comment='文件大小')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否删除: [0=否, 1=是]')


class AlbumCate(Base, TimestampMixin):
    __tablename__ = 'la_album_cate'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '相册分类表',
    }
    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键ID')
    pid = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='父级ID')
    type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('10'),
                  comment='文件类型: 10=图片,  20=视频')
    name = Column(String(100), nullable=False, server_default='', comment='分类名称')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否删除: [0=否, 1=是]')


common_album = Album.__table__
common_album_cate = AlbumCate.__table__
