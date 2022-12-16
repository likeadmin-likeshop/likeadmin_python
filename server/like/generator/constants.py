from typing import List
from typing_extensions import Final


class GenConstants:
    """代码生成常量"""
    UTF8: Final[str] = 'utf-8'  # 单表 (增删改查)
    TPL_CRUD: Final[str] = 'crud'  # 单表 (增删改查)
    TPL_TREE: Final[str] = 'tree'  # 树表 (增删改查)
    QUERY_LIKE: Final[str] = 'LIKE'  # 模糊查询
    QUERY_EQ: Final[str] = '='  # 相等查询
    REQUIRE: Final[int] = 1  # 需要的


class PyConstants:
    """Python相关常量"""
    TYPE_STRING: Final[str] = 'str'  # 字符串类型
    TYPE_FLOAT: Final[str] = 'float'  # 浮点型
    TYPE_INTEGER: Final[str] = 'int'  # 整型
    TYPE_DATE: Final[str] = 'datetime'  # 时间类型


class SqlConstants:
    """数据库相关常量"""
    # 数据库字符串类型
    COLUMN_TYPE_STR: Final[List[str]] = ['char', 'varchar', 'nvarchar', 'varchar2']
    # 数据库文本类型
    COLUMN_TYPE_TEXT: Final[List[str]] = ['tinytext', 'text', 'mediumtext', 'longtext']
    # 数据库时间类型
    COLUMN_TYPE_TIME: Final[List[str]] = ['datetime', 'time', 'date', 'timestamp']
    # 数据库数字类型
    COLUMN_TYPE_NUMBER: Final[List[str]] = [
        'tinyint', 'smallint', 'mediumint', 'int', 'number', 'integer', 'bit',
        'bigint', 'float', 'double', 'decimal']
    # 时间日期字段名
    COLUMN_TIME_NAME: Final[List[str]] = ['create_time', 'update_time', 'delete_time', 'start_time', 'end_time']
    # 页面不需要插入字段
    COLUMN_NAME_NOT_ADD: Final[List[str]] = ['id', 'is_delete', 'create_time', 'update_time', 'delete_time']
    # 页面不需要编辑字段
    COLUMN_NAME_NOT_EDIT: Final[List[str]] = ['is_delete', 'create_time', 'update_time', 'delete_time']
    # 页面不需要列表字段
    COLUMN_NAME_NOT_LIST: Final[List[str]] = ['id', 'intro', 'content', 'is_delete', 'delete_time']
    # 页面不需要查询字段
    COLUMN_NAME_NOT_QUERY: Final[List[str]] = ['is_delete', 'create_time', 'update_time', 'delete_time']


class HtmlConstants:
    """HTML相关常量"""
    HTML_INPUT: Final[str] = 'input'  # 文本框
    HTML_TEXTAREA: Final[str] = 'textarea'  # 文本域
    HTML_SELECT: Final[str] = 'select'  # 下拉框
    HTML_RADIO: Final[str] = 'radio'  # 单选框
    HTML_DATETIME: Final[str] = 'datetime'  # 日期控件
    HTML_IMAGE_UPLOAD: Final[str] = 'imageUpload'  # 图片上传控件
    HTML_FILE_UPLOAD: Final[str] = 'fileUpload'  # 文件上传控件
    HTML_EDITOR: Final[str] = 'editor'  # 富文本控件
