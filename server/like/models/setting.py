from sqlalchemy import Column, String, text
from sqlalchemy.dialects import mysql

from .base import Base, TimestampMixin

__all__ = [
    "DictType", "settings_dict_type", "DictData", "settings_dict_data"
]


class DictType(Base, TimestampMixin):
    """字典类型"""
    __tablename__ = "la_dict_type"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
        "mysql_row_format": "Dynamic",
        "mysql_auto_increment": "1",
        "comment": "字典类型表",
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment="主键ID")

    dict_name = Column(String(100), nullable=False, server_default="", comment="字典名称")
    dict_type = Column(String(100), nullable=False, server_default="", comment="字典类型")
    dict_remark = Column(String(100), nullable=False, server_default="", comment="字典备注")

    dict_status = Column(mysql.TINYINT(1, unsigned=True), nullable=False, comment="字典状态: 0=停用, 1=正常")
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text("0"),
                       comment="是否删除: [0=否, 1=是]")


settings_dict_type = DictType.__table__


class DictData(Base, TimestampMixin):
    """字典数据表"""
    __tablename__ = "la_dict_data"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
        "mysql_row_format": "Dynamic",
        "mysql_auto_increment": "1",
        "comment": "字典数据表",
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment="主键ID")
    type_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text("0"), comment="类型")
    name = Column(String(100), nullable=False, server_default="", comment="键名")
    value = Column(String(200), nullable=False, server_default="", comment="数值")
    remark = Column(String(200), nullable=False, server_default="", comment="备注")
    sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text("0"), comment="排序")
    status = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text("0"),
                    comment="状态: 0=停用, 1=正常")
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text("0"),
                       comment="是否删除: [0=否, 1=是]")


settings_dict_data = DictData.__table__
