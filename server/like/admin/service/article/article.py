from abc import ABC, abstractmethod

from like.admin.schemas.article import ArticleCateAddin, \
    ArticleCateEditIn, ArticleCateChangeIn, ArticleCateDeleteIn


class IArticleCateService(ABC):
    """
    文章服务基类(admin)
    """

    @abstractmethod
    async def add(self, add_in: ArticleCateAddin):
        """
        文章新增
        :return:
        """
        pass

    @abstractmethod
    async def edit(self, edit_in: ArticleCateEditIn):
        """
        文章编辑
        :return:
        """
        pass

    @abstractmethod
    async def delete(self, delete_in: ArticleCateDeleteIn):
        """
        文章删除
        :return:
        """
        pass

    @abstractmethod
    async def change(self, change_in: ArticleCateChangeIn):
        """
        文章状态修改
        :param change_in:
        :return:
        """
        pass
