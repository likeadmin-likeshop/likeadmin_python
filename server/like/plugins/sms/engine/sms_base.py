from six import with_metaclass

from like.utils.singleton_abstract_class_utils import AbstractFactoryClass


class SmsBase(with_metaclass(AbstractFactoryClass)):
    """
    SMS 抽象工厂类
    """
    engine = ''

    def send(self, **kwargs):
        raise NotImplementedError

    def get_status(self):
        raise NotImplementedError

    @classmethod
    def init(cls):
        from like.plugins.sms.engine.aliyun_sms import AliyunSms
        from like.plugins.sms.engine.tencent_sms import TencentSms
        _ = AliyunSms, TencentSms
        for sub_class in cls.__subclasses__():
            SmsBase.register(sub_class.engine, sub_class)
