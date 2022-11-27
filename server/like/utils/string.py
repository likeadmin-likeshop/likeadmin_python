import re


class StringUtil:
    """字符串工具类"""
    to_snake_pattern = re.compile(r'(?<!^)(?=[A-Z])')

    @classmethod
    def to_snake_case(cls, name: str) -> str:
        """驼峰命名转蛇形命名"""
        return cls.to_snake_pattern.sub('_', name).lower()

    @classmethod
    def to_camel_case(cls, name: str, is_upper=True) -> str:
        """蛇形命名转驼峰命名
            is_upper: 为True则首字母大写, 否则首字母小写
        """
        if not name:
            return name
        res = ''.join(word.title() for word in name.split('_'))
        if not is_upper:
            res = f'{res[0].lower()}{res[1:]}'
        return res
