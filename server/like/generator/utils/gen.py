from typing import Union, List
import time

from sqlalchemy import select, text, and_
from sqlalchemy.sql import Select
from databases.interfaces import Record

from like.config import get_settings
from like.generator.config import GenConfig
from like.generator.constants import PyConstants, GenConstants, SqlConstants, HtmlConstants
from like.utils.string import StringUtil

__all__ = ['GenUtil']


class GenUtil:
    """代码生成工具"""

    @staticmethod
    def get_db_tables_query(table_name: Union[str, None], table_comment: Union[str, None]) -> Select:
        """查询库中的数据表"""
        where = []
        if table_name:
            where.append(text(f'lower(table_name) like lower("%{table_name}%")'))
        if table_comment:
            where.append(text(f'lower(table_comment) like lower("%{table_comment}%")'))
        return select(text('table_name AS table_name, table_comment AS table_comment, '
                           'create_time AS create_time, update_time AS update_time')) \
            .where(
            and_(
                text('table_schema = (SELECT database())'),
                text('table_name NOT LIKE "qrtz_%"'),
                text('table_name NOT LIKE "gen_%"'),
                text('table_name NOT IN (select table_name from la_gen_table)'),
                *where)).select_from(text('information_schema.tables'))

    @staticmethod
    def get_db_tables_query_by_names(table_names: List[str]) -> Select:
        """根据表名集查询表"""
        tbl_list_str = ','.join([f'"{i}"' for i in table_names])
        return select(text('table_name AS table_name, table_comment AS table_comment, '
                           'create_time AS create_time, update_time AS update_time')) \
            .where(
            and_(
                text('table_schema = (SELECT database())'),
                text('table_name NOT LIKE "qrtz_%"'),
                text('table_name NOT LIKE "gen_%"'),
                text(f'table_name IN ({tbl_list_str})'))) \
            .select_from(text('information_schema.tables'))

    @staticmethod
    def get_db_table_columns_query_by_name(table_name: str) -> Select:
        """根据表名查询列信息"""
        return select(text(
            'column_name AS column_name,'
            '(CASE WHEN (is_nullable = "no" && column_key != "PRI") THEN "1" ELSE NULL END) AS is_required, '
            '(CASE WHEN column_key = "PRI" THEN "1" ELSE "0" END) AS is_pk, '
            'ordinal_position AS sort, column_comment AS column_comment, '
            '(CASE WHEN extra = "auto_increment" THEN "1" ELSE "0" END) AS is_increment, column_type AS column_type')) \
            .where(
            and_(
                text('table_schema = (SELECT database())'),
                text(f'table_name = "{table_name}"'))) \
            .select_from(text('information_schema.columns')).order_by(text('ordinal_position'))

    @classmethod
    def init_table(cls, table: Record) -> dict:
        """初始化表"""
        tbl_dict = dict(table)
        tbl_dict.update({
            'author_name': '',
            'entity_name': cls.to_class_name(table.table_name),
            'module_name': cls.to_module_name(table.table_name),
            'function_name': table.table_comment.replace('表', ''),
            'create_time': int(time.time()),
            'update_time': int(time.time()),
        })
        return tbl_dict

    @classmethod
    def init_column(cls, table_dict: dict, column: Record) -> dict:
        """初始化字段列"""
        col_dict = dict(column)
        is_pk = column.is_pk
        column_name = column.column_name
        column_type = cls.get_db_type(column.column_type)
        column_length = cls.get_column_length(column.column_type)
        col_dict.update({
            'table_id': table_dict.get('id'),
            'column_name': column_name,
            'column_comment': column.column_comment,
            'column_type': column.column_type,
            'column_length': column_length,
            # 'java_field': StringUtil.to_camel_case(column_name, is_upper=False),
            'java_field': column_name,
            'java_type': PyConstants.TYPE_STRING,
            'query_type': GenConstants.QUERY_EQ,
            'create_time': table_dict.get('create_time'),
            'update_time': table_dict.get('update_time'),
        })
        # 文本域组
        if column_type in SqlConstants.COLUMN_TYPE_STR + SqlConstants.COLUMN_TYPE_TEXT:
            col_dict['html_type'] = HtmlConstants.HTML_TEXTAREA \
                if int(column_length) >= 500 or column_type in SqlConstants.COLUMN_TYPE_TEXT \
                else HtmlConstants.HTML_INPUT
        # 日期字段
        elif column_type in SqlConstants.COLUMN_TYPE_TIME:
            col_dict['java_type'] = PyConstants.TYPE_DATE
            col_dict['html_type'] = HtmlConstants.HTML_DATETIME
        # 时间字段
        elif column_name in SqlConstants.COLUMN_TIME_NAME:
            col_dict['java_type'] = PyConstants.TYPE_INTEGER
            col_dict['html_type'] = HtmlConstants.HTML_DATETIME
        # 数字字段
        elif column_type in SqlConstants.COLUMN_TYPE_NUMBER:
            col_dict['html_type'] = HtmlConstants.HTML_INPUT
            if ',' in column_length:
                col_dict['java_type'] = PyConstants.TYPE_FLOAT
            else:
                col_dict['java_type'] = PyConstants.TYPE_INTEGER
        # 非必填字段
        if column_name in SqlConstants.COLUMN_NAME_NOT_EDIT:
            col_dict['is_required'] = 0
        # 需插入字段
        if column_name not in SqlConstants.COLUMN_NAME_NOT_ADD:
            col_dict['is_insert'] = GenConstants.REQUIRE
        # 需编辑字段
        if column_name not in SqlConstants.COLUMN_NAME_NOT_EDIT:
            col_dict['is_edit'] = GenConstants.REQUIRE
            col_dict['is_required'] = GenConstants.REQUIRE
        # 需列表字段
        if column_name not in SqlConstants.COLUMN_NAME_NOT_LIST and is_pk == '0':
            col_dict['is_list'] = GenConstants.REQUIRE
        # 需查询字段
        if column_name not in SqlConstants.COLUMN_NAME_NOT_QUERY and is_pk == '0':
            col_dict['is_query'] = GenConstants.REQUIRE
        lower_column_name = column_name.lower()
        # 模糊查字段
        if lower_column_name.endswith('name') or column_name in ['nickname', 'username', 'title', 'mobile']:
            col_dict['query_type'] = GenConstants.QUERY_LIKE
        # 根据字段设置
        if lower_column_name.endswith('status') or column_name in ['is_show', 'is_disable']:
            # 状态字段设置单选框
            col_dict['html_type'] = HtmlConstants.HTML_RADIO
        elif lower_column_name.endswith('type') or lower_column_name.endswith('sex'):
            # 类型&性别字段设置下拉框
            col_dict['html_type'] = HtmlConstants.HTML_SELECT
        elif lower_column_name.endswith('image'):
            # 类型&性别字段设置下拉框
            col_dict['html_type'] = HtmlConstants.HTML_IMAGE_UPLOAD
        elif lower_column_name.endswith('file'):
            # 类型&性别字段设置下拉框
            col_dict['html_type'] = HtmlConstants.HTML_FILE_UPLOAD
        elif lower_column_name.endswith('content'):
            # 类型&性别字段设置下拉框
            col_dict['html_type'] = HtmlConstants.HTML_EDITOR
        return col_dict

    @staticmethod
    def to_module_name(table_name: str) -> str:
        """表名转业务名"""
        return table_name.split('_')[-1]

    @staticmethod
    def to_class_name(table_name: str) -> str:
        """表名转类名"""
        table_prefix = get_settings().table_prefix
        if GenConfig.is_remove_table_prefix and table_prefix:
            table_name = table_name[len(table_prefix):] if table_name.startswith(table_prefix) else table_name
        return StringUtil.to_camel_case(table_name)

    @staticmethod
    def get_db_type(column_type: str) -> str:
        """获取数据库类型字段"""
        index = column_type.find('(')
        if index < 0:
            return column_type
        return column_type[:index]

    @staticmethod
    def get_column_length(column_type: str) -> str:
        """获取字段长度"""
        index = column_type.find('(')
        if index < 0:
            return '0'
        return column_type[index + 1:column_type.find(')')]

    @staticmethod
    def get_table_pri_col(columns: List[Record]) -> Record:
        """获取主键列名称"""
        pri_col = None
        for column in columns:
            if column.is_pk == '1':
                pri_col = column
        return pri_col
