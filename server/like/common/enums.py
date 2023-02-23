from enum import Enum


class SexEnum(int, Enum):
    """
    性别枚举
    """
    unknown = 0
    man = 1  # 男
    woman = 2  # 女

    @classmethod
    def key_list(cls):
        return list(map(lambda c: c.value, cls))


def get_sex(val):
    if not isinstance(val, int):
        return '未知'
    sex_dict = {
        1: '男',
        2: '女'
    }
    return sex_dict.get(val, '未知')


class LoginTypeEnum(str, Enum):
    """
    用户端登录方式枚举
    """
    account = 'account'  # 账号登录
    mnp = 'mnp'  # 微信登录
    mobile = 'mobile'  # 手机号登录
    office = 'office'  # 公众号登录


def get_login_type(val):
    type_dict = {
        'account': '账号登录',
        'mnp': '微信登录',
        'mobile': '手机号登录',
        'office': '公众号登录',
    }
    return type_dict.get(val, '未知')


class LoginClientEnum(int, Enum):
    """
    客户端类型枚举
    """
    MNP = 1  # ("微信小程序"),
    OA = 2  # ("微信公众号"),
    H5 = 3  # ("手机H5"),
    PC = 4  # ("电脑PC"),
    IOS = 5  # ("苹果APP"),
    APK = 6  # ("安卓APP");


def get_login_client(val):
    if not isinstance(val, int):
        return '未知'
    _dict = {
        1: '微信小程序',
        2: '微信公众号',
        3: '手机H5',
        4: '电脑PC',
        5: '苹果APP',
        6: '安卓APP',
    }
    return _dict.get(val, '未知')


class PageTypeEnum(int, Enum):
    """
    页面装修-页面类型枚举
    """
    HOME = 1  # 首页
    USER_CENTER = 2  # 个人中心
    CUSTOMER_SERVICE = 3  # 客服设置

class SmsEnum(int, Enum):
    LOGIN = 101,
    BIND_MOBILE = 102,
    CHANGE_MOBILE = 103,
    FIND_PASSWORD = 104
