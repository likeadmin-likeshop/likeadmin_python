from os import path
from typing import List

from jinja2 import Environment, FileSystemLoader, Template

from like.config import get_settings
from like.models.gen import GenTable, GenTableColumn
from like.utils.string import StringUtil
from .config import GenConfig
from .constants import GenConstants, SqlConstants

__all__ = ['TemplateUtil']


class TemplateUtil:
    """模板工具
        * 替换jinja2变量模板定界符,避免与vue冲突
            eg. {{ var }} => {{{ var }}}
    """
    env = Environment(loader=FileSystemLoader(path.join(path.dirname(path.abspath(__file__)), 'templates')),
                      variable_start_string='{{{', variable_end_string='}}}', keep_trailing_newline=True)

    @staticmethod
    def prepare_vars(table: GenTable, columns: List[GenTableColumn],
                     origin_pri_col: GenTableColumn = None, origin_cols: List[str] = None) -> dict:
        """获取模板变量信息"""

        origin_pri_field = 'id'
        is_search = False  # 是否需要搜索
        primary_key = 'id'  # 主键字段名称
        primary_field = 'id'  # 主键字段
        all_fields = []  # 所有字段
        sub_table_fields = []  # 子表字段
        list_fields = []  # 列表字段
        detail_fields = []  # 详情字段
        dict_fields = []  # 字典字段
        sub_columns = []  # 子表列
        if origin_cols is None:
            origin_cols = []
        if origin_pri_col:
            origin_pri_field = origin_pri_col.column_name
            sub_columns.append(origin_pri_col)
        for column in columns:
            all_fields.append(column.column_name)
            if column.column_name not in origin_cols:
                sub_table_fields.append(column.column_name)
                sub_columns.append(column)
            if column.is_list == 1:
                list_fields.append(column.column_name)
            if column.is_edit == 1:
                detail_fields.append(column.column_name)
            if column.is_query == 1:
                is_search = True
            if column.is_pk == 1:
                primary_key = column.java_field
                primary_field = column.column_name
            if column.dict_type and column.dict_type not in dict_fields:
                dict_fields.append(column.dict_type)
        # Python类型转换Sqlalchemy对应的类型
        model_type_map = {
            'str': 'String',
            'float': 'Float',
            'int': 'Integer',
            'datetime': 'Integer',
        }
        # query_type转换查询比较运算符
        model_opr_map = {
            '=': '==',
            'LIKE': 'like',
        }
        return {
            'gen_tpl': table.gen_tpl,
            'table_name': table.table_name,
            'author_name': table.author_name,
            'package_name': GenConfig.package_name,
            'entity_name': table.entity_name,
            'entity_snake_name': StringUtil.to_snake_case(table.entity_name),
            'module_name': table.module_name,
            'function_name': table.function_name if table.function_name else '【请填写功能名称】',
            'table': table,
            'columns': columns,
            'sub_columns': sub_columns,
            'java_camel_field': StringUtil.to_camel_case(column.java_field, is_upper=False),
            'date_fields': SqlConstants.COLUMN_TIME_NAME,
            'primary_key': primary_key,
            'primary_field': primary_field,
            'all_fields': all_fields,
            'sub_pri_col': origin_pri_col,
            'sub_pri_field': origin_pri_field,
            'sub_table_fields': sub_table_fields,
            'list_fields': list_fields,
            'detail_fields': detail_fields,
            'dict_fields': dict_fields,
            'is_search': is_search,
            'model_type_map': model_type_map,
            'model_opr_map': model_opr_map,
        }

    @staticmethod
    def get_gen_path(table: GenTable) -> str:
        """获取生成根路径"""
        gen_path = table.gen_path
        if gen_path == '/':
            return path.join(get_settings().root_path, 'target')
        return gen_path

    @staticmethod
    def get_file_path(tpl_path: str, module_name: str) -> str:
        """获取生成文件相对路径"""
        path_fmt_map = {
            'py/service.py.tpl': 'py/{module_name}/service.py',
            'py/schemas.py.tpl': 'py/{module_name}/schemas.py',
            'py/models.py.tpl': 'py/{module_name}/models.py',
            'py/routes.py.tpl': 'py/{module_name}/routes.py',
            'vue/api.ts.tpl': 'vue/{module_name}.ts',
            'vue/edit.vue.tpl': 'vue/{module_name}/edit.vue',
            'vue/index.vue.tpl': 'vue/{module_name}/index.vue',
            'vue/index-tree.vue.tpl': 'vue/{module_name}/index-tree.vue',
        }
        return path_fmt_map.get(tpl_path, '').format(module_name=module_name)

    @staticmethod
    def get_module_file_paths(module_name: str) -> List[str]:
        """获取Python模块文件相对路径"""
        return [
            'py/__init__.py',
            f'py/{module_name}/__init__.py',
        ]

    @staticmethod
    def get_template_paths(gen_tpl: str) -> List[str]:
        """获取模板文件路径"""
        tpl_paths = [
            'py/models.py.tpl',
            'py/routes.py.tpl',
            'py/schemas.py.tpl',
            'py/service.py.tpl',
            'vue/api.ts.tpl',
            'vue/edit.vue.tpl',
        ]
        if gen_tpl == GenConstants.TPL_CRUD:
            tpl_paths.append('vue/index.vue.tpl')
        elif gen_tpl == GenConstants.TPL_TREE:
            tpl_paths.append('vue/index-tree.vue.tpl')
        return tpl_paths

    @classmethod
    def get_template(cls, tpl_path: str) -> Template:
        """获取模板对象"""
        return cls.env.get_template(tpl_path)
