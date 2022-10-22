from sqlalchemy import Column, String, text
from sqlalchemy.dialects import mysql

from .base import Base

__all__ = ['SystemAuthAdmin', 'SystemLogLogin', 'system_auth_admin', 'system_log_login']


class SystemAuthAdmin(Base):
    __tablename__ = 'la_system_auth_admin'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '系统管理成员表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    dept_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='部门ID')
    post_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='岗位ID')
    username = Column(String(32), nullable=False, server_default='', comment='用户账号')
    nickname = Column(String(32), nullable=False, server_default='', comment='用户昵称')
    password = Column(String(200), nullable=False, server_default='', comment='用户密码')
    avatar = Column(String(200), nullable=False, server_default='', comment='用户头像')
    role = Column(String(200), nullable=False, server_default='', comment='角色主键')
    salt = Column(String(20), nullable=False, server_default='', comment='加密盐巴')
    sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text('0'), comment='排序编号')
    is_multipoint = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                           comment='多端登录: 0=否, 1=是')
    is_disable = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                        comment='是否禁用: [0=否, 1=是]')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否删除: [0=否, 1=是]')
    last_login_ip = Column(String(30), nullable=False, server_default='', comment='最后登录IP')
    last_login_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'),
                             comment='最后登录时间')
    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')
    delete_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='删除时间')


class SystemLogLogin(Base):
    __tablename__ = 'la_system_log_login'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '系统登录日志表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    admin_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='管理员ID')
    username = Column(String(32), nullable=False, server_default='', comment='登录账号')
    ip = Column(String(30), nullable=False, server_default='', comment='登录地址')
    os = Column(String(100), nullable=False, server_default='', comment='操作系统')
    browser = Column(String(100), nullable=False, server_default='', comment='浏览器')
    status = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                    comment='操作状态: 1=成功, 2=失败')
    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')


system_auth_admin = SystemAuthAdmin.__table__
system_log_login = SystemLogLogin.__table__
