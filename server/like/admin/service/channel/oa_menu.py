import json
from abc import ABC, abstractmethod

from like.admin.schemas.channel import ChannelOaMenusIn
from like.exceptions.base import AppException
from like.http_base import HttpResp
from like.utils.config import ConfigUtil
from like.utils.tools import ToolsUtil
from like.utils.wechat import WeChatUtil


class IChannelOaMenuService(ABC):
    """公众号菜单服务抽象类"""

    @abstractmethod
    async def detail(self) -> dict:
        pass

    @abstractmethod
    async def save(self, menus_in: ChannelOaMenusIn, is_publish: bool):
        pass


class ChannelOaMenuService(IChannelOaMenuService):
    """公众号菜单服务实现类"""

    async def detail(self) -> dict:
        """菜单详情"""
        config = await ConfigUtil.get_val('oa_channel', 'menus', '[]')
        return ToolsUtil.json_to_map(config)

    async def save(self, menus_in: ChannelOaMenusIn, is_publish: bool):
        """菜单保存"""
        menus = menus_in.dict().get('__root__')
        if len(menus) > 3:
            raise AppException(HttpResp.FAILED, msg='一级菜单超出限制(最多3个)')
        for item in menus:
            menu_type = item.pop('menu_type')
            # 一级菜单
            if menu_type == 1:
                item.pop('sub_button')
                assert item.get('type'), '一级菜单visitType数缺失'
                if item.get('type') == 'miniprogram':
                    assert item.get('appid'), '一级菜单appId参数缺失'
                    assert item.get('url'), '一级菜单url数缺失'
                    assert item.get('pagepath'), '一级菜单pagePath数缺失'
                else:
                    assert item.get('url'), '一级菜单url数缺失'
                    item.pop('appid')
                    item.pop('pagepath')
            # 子级菜单
            if menu_type == 2:
                item.pop('type')
                sub_buttons = item.get('sub_button')
                assert sub_buttons, '子级菜单不能为空'
                if len(sub_buttons) > 5:
                    raise AppException(HttpResp.FAILED, msg='子级菜单超出限制(最多5个)')
                for sub in sub_buttons:
                    assert sub.get('type'), '子级菜单visitType参数缺失!'
                    if sub.get('type') == 'miniprogram':
                        assert sub.get('appid'), '子级菜单appId参数缺失'
                        assert sub.get('url'), '子级菜单url数缺失'
                        assert sub.get('pagepath'), '子级菜单pagePath数缺失'
                    else:
                        assert sub.get('url'), '子级菜单url数缺失'
                        sub.pop('appid')
                        sub.pop('pagepath')
        await ConfigUtil.set('oa_channel', 'menus', json.dumps(menus))
        if is_publish:
            client = await WeChatUtil.official()
            client.menu.create({
                'button': menus
            })

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
