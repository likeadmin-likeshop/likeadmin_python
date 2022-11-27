import sqlalchemy as sa

from {{{ package_name }}}.models.base import Base


class {{{ entity_name }}}(Base):
    """{{{ function_name }}}实体"""
    __tablename__ = 'la_{{{ entity_snake_name }}}'
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_general_ci',
        'mysql_row_format': 'Dynamic',
        'comment': '{{{ function_name }}}表',
    }

    {%- for column in columns %}
    {%- if column.column_name not in sub_table_fields %}
    {{{ column.java_field }}} = sa.Column(sa.{{{ model_type_map.get(column.java_type) or column.java_type }}}(){% if column.is_pk %}, primary_key=True{% endif %})  # {{{ column.column_comment }}}
    {%- endif %}
    {%- endfor %}


{{{ entity_snake_name }}} = {{{ entity_name }}}.__table__
