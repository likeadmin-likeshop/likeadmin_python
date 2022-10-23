from typing import Final


class AdminConfig:
    """后台公共配置"""
    # 管理缓存键
    backstage_manage_key: Final[str] = 'backstage:manage'
    # 角色缓存键
    backstage_roles_key: Final[str] = 'backstage:roles'
    # 令牌缓存键
    backstage_token_key: Final[str] = 'backstage:token:'
    # 令牌的集合
    backstage_token_set: Final[str] = 'backstage:token:set:'

    # 免登录验证
    not_login_uri = [
        'system:login',  # 登录接口
        'common:index:config',  # 配置接口
    ]

    # 免权限验证
    not_auth_uri = [
        'system:logout',  # 退出登录
        'system:menu:menus',  # 系统菜单
        'system:menu:route',  # 菜单路由
        'system:admin:upInfo',  # 管理员更新
        'system:admin:self',  # 管理员信息
        'system:role:all',  # 所有角色
        'system:post:all',  # 所有岗位
        'system:dept:list',  # 所有部门
        'setting:dict:type:all',  # 所有字典类型
        'setting:dict:data:all',  # 所有字典数据
        'article:cate:all',  # 所有文章分类
    ]
