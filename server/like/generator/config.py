from typing_extensions import Final


class GenConfig:
    """代码生成器公共配置"""

    # 基础包名
    package_name: Final[str] = 'like'
    # 后台包名
    admin_package: Final[str] = 'like.admin'
    # 实体包名
    models_package: Final[str] = 'like.models'
    # 是否去除表前缀
    is_remove_table_prefix: Final[bool] = True
    # 生成代码根路径
    gen_root_path: Final[str] = 'target'
