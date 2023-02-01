from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects import mysql

from .base import Base, TimestampMixin

__all__ = [
    "Article", "article_table", "ArticleCateGory", "article_cate_table"
]


class Article(Base, TimestampMixin):
    """文章资讯表"""
    __tablename__ = "la_article"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
        "mysql_row_format": "Dynamic",
        "mysql_auto_increment": "1",
        "comment": "文章资讯表",
    }

    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment="主键ID")
    cid = Column(mysql.INTEGER(10, unsigned=True), nullable=False, index=True, comment='分类ID')
    title = Column(String(200), nullable=False, server_default="", comment="标题")
    intro = Column(String(200), nullable=False, server_default="", comment="简介")
    summary = Column(String(200), nullable=False, server_default="", comment="摘要")
    image = Column(String(200), nullable=False, server_default="", comment="封面")
    content = Column(Text, nullable=False, server_default="", comment="内容")
    author = Column(String(32), nullable=False, server_default="", comment="作者")
    visit = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text("0"), comment="浏览")
    sort = Column(mysql.INTEGER(10, unsigned=True), nullable=False, server_default=text("50"), comment="排序")
    is_show = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('1'),
                     comment='是否显示: 0=否, 1=是')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text("0"),
                       comment="是否删除: 0=否, 1=是")


class ArticleCateGory(Base, TimestampMixin):
    """
    文章分类表
    """
    __tablename__ = "la_article_category"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
        "mysql_row_format": "Dynamic",
        "mysql_auto_increment": "1",
        "comment": "文章分类表",
    }
    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment="主键ID")
    name = Column(String(60), nullable=False, server_default="", comment="名称")
    sort = Column(mysql.SMALLINT(5), nullable=False, server_default=text("50"), comment="排序")
    is_show = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text('1'),
                     comment='是否显示: 0=否, 1=是')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text("0"),
                       comment="是否删除: 0=否, 1=是")


class ArticleCollect(Base, TimestampMixin):
    """
    文章收藏表
    """
    __tablename__ = "la_article_collect"
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_general_ci",
        "mysql_row_format": "Dynamic",
        "mysql_auto_increment": "1",
        "comment": "文章收藏表",
    }
    id = Column(mysql.INTEGER(10, unsigned=True), primary_key=True, comment="主键ID")
    user_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, comment='用户ID')
    article_id = Column(mysql.INTEGER(10, unsigned=True), nullable=False, comment='文章ID')
    is_delete = Column(mysql.TINYINT(1, unsigned=True), nullable=False, server_default=text("0"),
                       comment="是否删除: 0=否, 1=是")


article_table = Article.__table__
article_cate_table = ArticleCateGory.__table__
article_collect_table = ArticleCollect.__table__
