from abc import ABC, abstractmethod
from typing import List

import pydantic
import sqlalchemy as sa
from fastapi_pagination.bases import AbstractPage
from fastapi_pagination.ext.databases import paginate

from {{{ package_name }}}.dependencies.database import db
from {{{ package_name }}}.utils.urls import UrlUtil
from {{{ package_name }}}.utils.array import ArrayUtil
from .models import {{{ entity_snake_name }}}
from .schemas import (
    {{{ entity_name }}}ListIn, {{{ entity_name }}}AddIn, {{{ entity_name }}}EditIn, {{{ entity_name }}}Out)


class I{{{ entity_name }}}Service(ABC):
    """{{{ function_name }}}抽象类"""

    @abstractmethod
    async def list(self, list_in: {{{ entity_name }}}ListIn) -> {% if table.gen_tpl == 'tree' %}List{% else %}AbstractPage{% endif %}[{{{ entity_name }}}Out]:
        pass

    @abstractmethod
    async def detail(self, id_: int) -> {{{ entity_name }}}Out:
        pass

    @abstractmethod
    async def add(self, add_in: {{{ entity_name }}}AddIn):
        pass

    @abstractmethod
    async def edit(self, edit_in: {{{ entity_name }}}EditIn):
        pass

    @abstractmethod
    async def delete(self, id_: int):
        pass


class {{{ entity_name }}}Service(I{{{ entity_name }}}Service):
    """{{{ function_name }}}实现类"""

    async def list(self, list_in: {{{ entity_name }}}ListIn) -> {% if table.gen_tpl == 'tree' %}List[dict]{% else %}AbstractPage[{{{ entity_name }}}Out]{% endif %}:
        """{{{ function_name }}}列表"""
        columns = [
            {{{ entity_snake_name }}},
            {% if table.sub_table_name and table.sub_table_fk and sub_table_fields %}sa.text(','.join(({% for field in sub_table_fields %}'{{{ field }}}', {% endfor %}))){% endif %}
            ]
        {%- if table.sub_table_name and table.sub_table_fk and sub_table_fields %}
        sub_table = sa.text('SELECT * FROM la_{{{ table.sub_table_name }}}') \
            .columns({% for sub_column in sub_columns %}{{{ sub_column.column_name }}}=sa.{{{ model_type_map.get(sub_column.java_type) or sub_column.java_type }}}, {% endfor %})
        {%- endif %}
        where = []
        {%- for column in columns %}
        {%- if column.is_query %}
        if list_in.{{{ column.column_name }}} is not None:
        {%- set query_opr = model_opr_map.get(column.query_type) or column.query_type %}
        {%- if column.column_name in sub_table_fields %}
            {%- if column.java_type == 'str' and query_opr == 'like' %}
            where.append(sa.text(f'{{{ column.column_name }}} like "%{list_in.{{{ column.column_name }}}}%"'))
            {%- elif query_opr == '==' %}
            where.append(sa.text(f'{{{ column.column_name }}} = {% if column.java_type == 'str' %}"{% endif %}{ list_in.{{{ column.column_name }}} }{% if column.java_type == 'str' %}"{% endif %}'))
            {%- else %}
            where.append(sa.text(f'{{{ column.column_name }}} {{{ query_opr }}} {% if column.java_type == 'str' %}"{% endif %}{ list_in.{{{ column.column_name }}} }{% if column.java_type == 'str' %}"{% endif %}'))
            {%- endif %}
        {%- else %}
            {%- if column.java_type == 'str' and query_opr == 'like' %}
            where.append({{{ entity_snake_name }}}.c.{{{ column.column_name }}}.like(f'%{ list_in.{{{ column.column_name }}} }%'))
            {%- else %}
            where.append({{{ entity_snake_name }}}.c.{{{ column.column_name }}} {{{ query_opr }}} {% if column.java_type == 'datetime' %}int(time.mktime({% endif %}list_in.{{{ column.column_name }}}{% if column.java_type == 'datetime' %}.timetuple()){% endif %})
            {%- endif %}
        {%- endif %}
        {%- endif %}
        {%- endfor %}
        {%- if 'is_delete' in all_fields %}
        where.append({{{ entity_snake_name }}}.c.is_delete == 0)
        {%- endif %}
        query = sa.select(columns).where(*where) \
            .select_from(
            {{{ entity_snake_name }}}
            {%- if table.sub_table_name and table.sub_table_fk and sub_table_fields %}
                .outerjoin(sub_table, {{{ entity_snake_name }}}.c.{{{ table.sub_table_fk }}} == sub_table.c.{{{ sub_pri_field }}})
            {%- endif %}
        {%- if 'sort' in all_fields %}
        ).order_by({{{ entity_snake_name }}}.c.sort.desc(), {{{ entity_snake_name }}}.c.id.desc())
        {%- else %}
        ).order_by({{{ entity_snake_name }}}.c.id.desc())
        {%- endif %}
        {%- if table.gen_tpl == 'tree' %}
        data = await db.fetch_all(query)
        res = ArrayUtil.list_to_tree(
            [i.dict(exclude_none=True) for i in pydantic.parse_obj_as(List[{{{ entity_name }}}Out], data)],
            '{{{ table.tree_primary }}}', '{{{ table.tree_parent }}}', 'children')
        {%- else %}
        res = await paginate(db, query)
        {%- endif %}
        return res

    async def detail(self, id_: int) -> {{{ entity_name }}}Out:
        """{{{ function_name }}}详情"""
        model = await db.fetch_one(
            {{{ entity_snake_name }}}.select().where(
                {{{ entity_snake_name }}}.c.{{{ primary_key }}} == id_{% if 'is_delete' in all_fields %}, {{{ entity_snake_name }}}.c.is_delete == 0{%- endif %})
            .limit(1))
        assert model, '数据不存在!'
        res = {{{ entity_name }}}Out.from_orm(model)
        {%- for column in columns %}
        {%- if column.is_edit and column.java_field in ['image', 'avatar', 'logo', 'img'] %}
        res.{{{ column.java_field }}} = UrlUtil.to_relative_url(res.{{{ column.java_field }}})
        {%- endif %}
        {%- endfor %}
        return res

    async def add(self, add_in: {{{ entity_name }}}AddIn):
        """{{{ function_name }}}新增"""
        await db.execute({{{ entity_snake_name }}}.insert().values({
            {%- for column in columns %}
            {%- if (column.is_insert or column.column_name in ['create_time', 'update_time']) and column.is_pk == 0 %}
            {%- if column.java_field in ['image', 'avatar', 'logo', 'img'] %}
            '{{{ column.java_field }}}': UrlUtil.to_relative_url(add_in.{{{ column.java_field}}}),
            {%- elif column.column_name not in date_fields and column.java_field != 'is_delete' %}
            '{{{ column.java_field }}}': add_in.{{{ column.java_field}}},
            {%- elif column.java_type == 'datetime' %}
            '{{{ column.java_field }}}': int(time.time()),
            {%- endif %}
            {%- endif %}
            {%- endfor %}
        }))

    async def edit(self, edit_in: {{{ entity_name }}}EditIn):
        """{{{ function_name }}}编辑"""
        assert await db.fetch_one(
            {{{ entity_snake_name }}}.select().where(
                {{{ entity_snake_name }}}.c.{{{ primary_key }}} == edit_in.id{% if 'is_delete' in all_fields %}, {{{ entity_snake_name }}}.c.is_delete == 0{%- endif %})
            .limit(1)), '数据不存在!'
        await db.execute(
            {{{ entity_snake_name }}}.update().where({{{ entity_snake_name }}}.c.{{{ primary_key }}} == edit_in.id).values({
                {%- for column in columns %}
                {%- if (column.is_edit or column.column_name == 'update_time') and column.is_pk == 0 %}
                {%- if column.java_field in ['image', 'avatar', 'logo', 'img'] %}
                '{{{ column.java_field }}}': UrlUtil.to_relative_url(edit_in.{{{ column.java_field}}}),
                {%- elif column.column_name not in date_fields and column.java_field != 'is_delete' %}
                '{{{ column.java_field }}}': edit_in.{{{ column.java_field}}},
                {%- elif column.java_type == 'datetime' and column.column_name == 'update_time' %}
                '{{{ column.java_field }}}': int(time.time()),
                {%- endif %}
                {%- endif %}
                {%- endfor %}
            }))

    async def delete(self, id_: int):
        """{{{ function_name }}}删除"""
        assert await db.fetch_one(
            {{{ entity_snake_name }}}.select().where(
                {{{ entity_snake_name }}}.c.{{{ primary_key }}} == id_{% if 'is_delete' in all_fields %}, {{{ entity_snake_name }}}.c.is_delete == 0{%- endif %})
            .limit(1)), '数据不存在!'
        {%- if 'is_delete' in all_fields %}
        await db.execute(
            {{{ entity_snake_name }}}.update().where({{{ entity_snake_name }}}.c.{{{ primary_key }}} == id_).values({
                'is_delete': 1,
                'delete_time': int(time.time()),
            }))
        {%- else %}
        await db.execute({{{ entity_snake_name }}}.delete().where({{{ entity_snake_name }}}.c.{{{ primary_key }}} == id_))
        {%- endif %}
        
    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
