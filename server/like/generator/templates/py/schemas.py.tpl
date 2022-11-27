from typing import Union

from fastapi import Query
from pydantic import BaseModel, Field


class {{{ entity_name }}}ListIn(BaseModel):
    """{{{ function_name }}}列表参数"""
    {%- for column in columns %}
    {%- if column.is_query %}
    {{{ column.java_field }}}: Union[{{{ column.java_type }}}, None] = Query()  # {{{ column.column_comment }}}
    {%- endif %}
    {%- endfor %}


class {{{ entity_name }}}DetailIn(BaseModel):
    """{{{ function_name }}}详情参数"""
    {%- for column in columns %}
    {%- if column.is_pk %}
    {{{ column.java_field }}}: {{{ column.java_type }}} = Query(gt=0)  # {{{ column.column_comment }}}
    {%- endif %}
    {%- endfor %}


class {{{ entity_name }}}AddIn(BaseModel):
    """{{{ function_name }}}新增参数"""
    {%- for column in columns %}
    {%- if column.is_insert %}
    {{{ column.java_field }}}: {% if column.is_required %}{{{ column.java_type }}}{% else %}Union[{{{ column.java_type }}}, None]{% endif %}  # {{{ column.column_comment }}}
    {%- endif %}
    {%- endfor %}


class {{{ entity_name }}}EditIn(BaseModel):
    """{{{ function_name }}}编辑参数"""
    {%- for column in columns %}
    {%- if column.is_edit %}
    {{{ column.java_field }}}: {% if column.is_required %}{{{ column.java_type }}}{% else %}Union[{{{ column.java_type }}}, None]{% endif %}{%- if column.is_pk %} = Field(gt=0){% endif %}  # {{{ column.column_comment }}}
    {%- endif %}
    {%- endfor %}


class {{{ entity_name }}}DelIn(BaseModel):
    """{{{ function_name }}}删除参数"""
    {%- for column in columns %}
    {%- if column.is_pk %}
    {{{ column.java_field }}}: {{{ column.java_type }}} = Field(gt=0)  # {{{ column.column_comment }}}
    {%- endif %}
    {%- endfor %}


class {{{ entity_name }}}Out(BaseModel):
    """{{{ function_name }}}返回信息"""
    {%- for column in columns %}
    {%- if column.is_list or column.is_pk %}
    {{{ column.java_field }}}: {{{ column.java_type }}}  # {{{ column.column_comment }}}
    {%- endif %}
    {%- endfor %}
    {%- if table.gen_tpl == 'tree' %}
    children: Union['{{{ entity_name }}}Out', None]  # 子集
    {%- endif %}

    class Config:
        orm_mode = True
