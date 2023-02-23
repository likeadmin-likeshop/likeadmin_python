from typing import List

from pydantic import BaseModel

from like.front.schemas.article import ArticleDetailOut


class IndexOut(BaseModel):
    domain: str
    pages: str
    article: List[ArticleDetailOut]
