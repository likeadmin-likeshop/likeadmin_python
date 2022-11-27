from sqlalchemy import Column, String, text
from sqlalchemy.dialects import mysql

from .base import Base

__all__ = [
    'GenTable', 'GenTableColumn',
    'gen_table', 'gen_table_column',
]


class GenTable(Base):
    """代码生成业务实体"""
    __tablename__ = 'la_gen_table'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '代码生成业务表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='主键')
    table_name = Column(String(200), nullable=True, server_default='', comment='表名称')
    table_comment = Column(String(200), nullable=True, server_default='', comment='表描述')
    sub_table_name = Column(String(200), nullable=True, server_default='', comment='关联表名称')
    sub_table_fk = Column(String(200), nullable=True, server_default='', comment='关联表外键')
    author_name = Column(String(200), nullable=True, server_default='', comment='作者的名称')
    entity_name = Column(String(200), nullable=True, server_default='', comment='实体的名称')
    module_name = Column(String(60), nullable=True, server_default='', comment='生成模块名')
    function_name = Column(String(60), nullable=True, server_default='', comment='生成功能名')
    tree_primary = Column(String(60), nullable=True, server_default='', comment='树主键字段')
    tree_parent = Column(String(60), nullable=True, server_default='', comment='树父级字段')
    tree_name = Column(String(60), nullable=True, server_default='', comment='树显示字段')
    gen_tpl = Column(String(20), nullable=True, server_default='crud', comment='生成模板方式: [crud=单表, tree=树表]')
    gen_type = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                      comment='生成代码方式: [0=zip压缩包, 1=自定义路径]')
    gen_path = Column(String(200), nullable=True, server_default='/', comment='生成代码路径: [不填默认项目路径]')
    remarks = Column(String(200), nullable=True, server_default='', comment='备注信息')
    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')


class GenTableColumn(Base):
    """代码生成表列实体"""
    __tablename__ = 'la_gen_table_column'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'mysql_auto_increment': '1',
        'comment': '代码生成字段表',
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment='列主键')
    table_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='表外键')
    column_name = Column(String(200), nullable=True, server_default='', comment='列名称')
    column_comment = Column(String(200), nullable=True, server_default='', comment='列描述')
    column_length = Column(String(5), nullable=True, server_default='0', comment='列长度')
    column_type = Column(String(100), nullable=True, server_default='', comment='列类型')
    java_type = Column(String(100), nullable=True, server_default='', comment='类型')
    java_field = Column(String(100), nullable=True, server_default='', comment='字段')
    is_pk = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                   comment='是否主键: [1=是, 0=否]')
    is_increment = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                          comment='是否自增: [1=是, 0=否]')
    is_required = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                         comment='是否必填: [1=是, 0=否]')
    is_insert = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                       comment='是否插入字段: [1=是, 0=否]')
    is_edit = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                     comment='是否编辑字段: [1=是, 0=否]')
    is_list = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                     comment='是否列表字段: [1=是, 0=否]')
    is_query = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('0'),
                      comment='是否查询字段: [1=是, 0=否]')
    query_type = Column(String(30), nullable=True, server_default='=',
                        comment='查询方式: [等于、不等于、大于、小于、范围]')
    html_type = Column(String(30), nullable=True, server_default='',
                       comment='显示类型: [文本框、文本域、下拉框、复选框、单选框、日期控件]')
    dict_type = Column(String(200), nullable=True, server_default='', comment='字典类型')
    sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text('0'), comment='排序编号')
    create_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='创建时间')
    update_time = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text('0'), comment='更新时间')


gen_table = GenTable.__table__
gen_table_column = GenTableColumn.__table__
