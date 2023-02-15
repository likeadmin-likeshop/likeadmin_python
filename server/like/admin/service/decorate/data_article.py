from abc import ABC, abstractmethod
from typing import List

from fastapi import Depends

from like.admin.schemas.article import ArticleListOut
from like.admin.schemas.decorate import DecorateDataArticleIn
from like.admin.service.article.article import IArticleService, ArticleService
from like.models.decorate import decorate_page


class IDecorateArticleService(ABC):
    @abstractmethod
    async def data_article(self, article_in: DecorateDataArticleIn) -> List[ArticleListOut]:
        pass


class DecorateArticleService(ABC):
    select_columns = [decorate_page.c.id, decorate_page.c.page_type, decorate_page.c.page_data]

    async def data_article(self, article_in: DecorateDataArticleIn) -> List[ArticleListOut]:
        return await self.article_service.list_limit(article_in.limit)

    @classmethod
    def __init__(self, article_service: IArticleService):
        self.article_service: IArticleService = article_service

    @classmethod
    async def instance(cls, article_service: IArticleService = Depends(ArticleService.instance)):
        """实例化"""
        return cls(article_service)
