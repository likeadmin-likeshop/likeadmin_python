import json
from abc import ABC, abstractmethod
from datetime import date, timedelta

from like.config import get_settings
from like.utils.config import ConfigUtil
from like.utils.urls import UrlUtil


class IIndexService(ABC):
    """主页服务抽象类"""

    @abstractmethod
    async def console(self) -> dict:
        pass

    @abstractmethod
    async def config(self) -> dict:
        pass


class IndexService(IIndexService):
    """主页服务实现类"""

    async def console(self) -> dict:
        """控制台数据"""
        today = date.today()
        return {
            # 版本信息
            'version': {
                'name': await ConfigUtil.get_val('website', 'name', 'LikeAdmin-Python'),
                'version': get_settings().version,
                'website': 'www.likeadmin.cn',
                'based': 'Vue3.x、ElementUI、MySQL',
                'channel': {
                    'gitee': 'https://gitee.com/likeadmin/likeadmin_python',
                    'website': 'https://www.likeadmin.cn',
                }
            },
            # 今日数据
            'today': {
                'time': '2022-08-11 15:08:29',
                'todayVisits': 10,  # 访问量(人)
                'totalVisits': 100,  # 总访问量
                'todaySales': 30,  # 销售额(元)
                'totalSales': 65,  # 总销售额
                'todayOrder': 12,  # 订单量(笔)
                'totalOrder': 255,  # 总订单量
                'todayUsers': 120,  # 新增用户
                'totalUsers': 360,  # 总访用户
            },
            # 访客图表
            'visitor': {
                'date': [(today - timedelta(days=i)).isoformat() for i in range(14, -1, -1)],
                'list': [12, 13, 11, 5, 8, 22, 14, 9, 456, 62, 78, 12, 18, 22, 46],
            }
        }

    async def config(self) -> dict:
        """公共配置"""
        website = await ConfigUtil.get('website')
        copyright = await ConfigUtil.get_val('website', 'copyright', '')
        return {
            'webName': website.get('name', ''),
            'webLogo': website.get('logo', ''),
            'webFavicon': website.get('favicon', ''),
            'webBackdrop': website.get('backdrop', ''),
            'ossDomain': UrlUtil.domain,
            'copyright': json.loads(copyright) if copyright else [],
        }

    @classmethod
    async def instance(cls):
        """实例化"""
        return cls()
