# -*- coding:utf-8 -*-
from __future__ import absolute_import


class SingletonMetaClass(type):
    """
    单例类元类
    """
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonMetaClass, cls).__call__(*args, **kwargs)
        return cls._instance


class AbstractFactoryClass(SingletonMetaClass):
    """
    抽象工厂元类
    """

    def __init__(cls, *args, **kwargs):
        super(AbstractFactoryClass, cls).__init__(*args, **kwargs)
        cls.instances = {}
        cls._initialed = False

    def register(cls, name, subclass):
        """
        向基类注册
        """
        if name in cls.instances:
            raise ValueError("subclass name: %s has been registered" % name)
        else:
            cls.instances[name] = subclass

    def getInstance(cls, name):
        """
        通过类的名字获得 子类 的实例(因为是singleton)
        """
        if not cls._initialed:
            cls.init()
            cls._initialed = True
        if name not in cls.instances:
            registered_name = ', '.join(list(cls.instances.keys()))
            raise ValueError("name: %s has not been registered.\n Registered name is:\n%s" % (name, registered_name))
        else:
            return cls.instances[name]()

    def remove(cls, name, subclass):
        """
        动态删除某个子类
        """
        if name not in cls.instances:
            raise ValueError("subclass name: %s has not been registered" % name)
        if cls.instances[name] != subclass:
            raise ValueError("registered subclass and removed subclass not the same")
        else:
            del cls.instances[name]

    def init(cls):
        """
        初始化操作，把子类注册全部引入
        """
        raise NotImplementedError
