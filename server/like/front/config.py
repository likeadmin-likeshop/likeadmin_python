from enum import Enum


class LoginTypeEnum(str, Enum):
    """
    登录方式枚举
    """
    account = 'account'  # 账号登录
    mnp = 'mnp'  # 微信登录
    mobile = 'mobile'  # 手机号登录
    office = 'office'  # 公众号登录


class LoginClientEnum(int, Enum):
    MNP = 1  # (1, "微信小程序"),
    OA = 2  # ("微信公众号"),
    H5 = 3  # ("手机H5"),
    PC = 4  # ("电脑PC"),
    IOS = 5  # ("苹果APP"),
    APK = 6  # ("安卓APP");


class FrontConfig:
    """前台公共配置"""

    # 登录缓存键
    frontendTokenKey = "frontend:token:"

    # 登录有效时间 (单位秒)
    token_valid_time = 7200
    # 登录续签时间 (不足以下秒数续签)
    token_renew_time = 1800

    #  免登录验证
    not_login_uri = [
        "/api/index",
        "/api/config",
        "/api/policy",
        "/api/search",
        "/api/hotSearch",
        "/api/decorate",
        "/api/sms/send",
        "/api/upload/image",

        "/api/login/check",
        "/api/login/codeUrl",
        "/api/login/oaLogin",
        "/api/login/register",
        "/api/login/forgotPassword",

        "/api/article/category",
        "/api/article/detail",
        "/api/article/list",
        "/api/pc/getConfig",
        "/api/pc/index",
        "/api/pc/articleCenter",
        "/api/pc/articleDetail",
        "/api/login/getScanCode",
        "/api/login/scanLogin"
    ]
