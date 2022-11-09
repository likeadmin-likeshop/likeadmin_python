import logging
import socket

logger = logging.getLogger(__name__)


class IpUtil:
    """IP工具类"""

    @staticmethod
    def get_host_name() -> str:
        """获取本地IP地址"""
        return socket.gethostname()

    @staticmethod
    def get_host_ip() -> str:
        """获取本地主机名"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.0.0.0', 0))
            ip = s.getsockname()[0]
        except Exception as _:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip
