from sqlalchemy import Column, String, text
from sqlalchemy.dialects import mysql

from .base import Base, TimestampMixin

__all__ = [
    'SystemAuthAdmin', 'SystemAuthMenu', 'SystemAuthPerm', 'SystemAuthRole', 'SystemLogLogin', 'SystemAuthDept',
    'SystemAuthPost', 'system_auth_admin', 'system_auth_menu', 'system_auth_perm', 'system_auth_role',
    'system_log_login',
    'system_auth_post', 'system_auth_dept'
]


class SystemAuthAdmin(Base):
    """系统管理员实体"""
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


class SystemAuthMenu(Base):
    """系统菜单实体"""
    __tablename__ = 'la_system_auth_menu'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '系统菜单管理表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    pid = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='上级菜单')
    menu_type = Column(mysql.CHAR(2), nullable=False, server_default='', comment='权限类型: M=目录，C=菜单，A=按钮')
    menu_name = Column(String(100), nullable=False, server_default='', comment='菜单名称')
    menu_icon = Column(String(100), nullable=False, server_default='', comment='菜单图标')
    menu_sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text('0'), comment='菜单排序')
    perms = Column(String(100), nullable=False, server_default='', comment='权限标识')
    paths = Column(String(100), nullable=False, server_default='', comment='路由地址')
    component = Column(String(200), nullable=False, server_default='', comment='前端组件')
    selected = Column(String(200), nullable=False, server_default='', comment='选中路径')
    params = Column(String(200), nullable=False, server_default='', comment='路由参数')
    is_cache = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                      comment='是否缓存: 0=否, 1=是')
    is_show = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('1'),
                     comment='是否显示: 0=否, 1=是')
    is_disable = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                        comment='是否禁用: 0=否, 1=是')
    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')


class SystemAuthPerm(Base):
    """系统角色菜单实体"""
    __tablename__ = 'la_system_auth_perm'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '系统角色菜单表',
    }

    id = Column(String(100), primary_key=True, server_default='', comment='主键')
    role_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='角色ID')
    menu_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='菜单ID')


class SystemAuthRole(Base):
    """系统角色实体"""
    __tablename__ = 'la_system_auth_role'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '系统角色管理表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    name = Column(String(100), nullable=False, server_default='', comment='角色名称')
    remark = Column(String(200), nullable=False, server_default='', comment='备注信息')
    is_disable = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                        comment='是否禁用: 0=否, 1=是')
    sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text('0'), comment='角色排序')
    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')


class SystemLogLogin(Base):
    """系统登录日志实体"""
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


class SystemAuthDept(Base, TimestampMixin):
    __tablename__ = 'la_system_auth_dept'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '系统部门管理表',
    }
    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    pid = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='上级主键')
    name = Column(String(100), nullable=False, server_default='', comment='部门名称')
    duty = Column(String(30), nullable=False, server_default='', comment='负责人名')
    mobile = Column(String(30), nullable=False, server_default='', comment='联系电话')
    sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text('0'), comment='排序编号')
    is_stop = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                     comment='是否停用: 0=否, 1=是')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否删除: [0=否, 1=是]')


class SystemAuthPost(Base, TimestampMixin):
    __tablename__ = 'la_system_auth_post'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '系统岗位管理表',
    }
    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    code = Column(String(30), nullable=False, server_default=text('0'), comment='岗位编码')
    name = Column(String(30), nullable=False, server_default='', comment='岗位名称')
    remarks = Column(String(250), nullable=False, server_default='', comment='岗位备注')
    sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text('0'), comment='排序编号')
    is_stop = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                     comment='是否停用: 0=否, 1=是')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否删除: [0=否, 1=是]')


system_auth_admin = SystemAuthAdmin.__table__
system_auth_menu = SystemAuthMenu.__table__
system_auth_perm = SystemAuthPerm.__table__
system_auth_role = SystemAuthRole.__table__
system_log_login = SystemLogLogin.__table__
system_auth_post = SystemAuthPost.__table__
system_auth_dept = SystemAuthDept.__table__
