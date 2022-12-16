import os
import platform
import sys
from datetime import datetime, timedelta
from typing import List, Any

import psutil

from like.config import get_settings
from like.utils.ip import IpUtil


def get_attr(obj: Any, attr: str, default: Any = None) -> Any:
    return getattr(obj, attr, default)


class ServerInfo:
    """服务器相关信息"""
    datetime_fmt = get_settings().datetime_fmt

    @staticmethod
    def get_size(data, suffix='B') -> str:
        """
        按照正确的格式缩放字节
        eg:
            1253656 => '1.20MB'
            1253656678 => '1.17GB'
        """
        factor = 1024
        for unit in ['', 'K', 'M', 'G', 'T', 'P']:
            if data < factor:
                return f'{data:.2f}{unit}{suffix}'
            data /= factor

    @staticmethod
    def fmt_timedelta(td: timedelta) -> str:
        """格式化显示timedelta
        eg:
            timedelta => xx天xx小时xx分钟
        """
        rem = td.seconds
        days, rem = rem // 86400, rem % 86400
        hours, rem = rem // 3600, rem % 3600
        minutes = rem // 60
        res = f'{minutes}分钟'
        if hours > 0:
            res = f'{hours}小时{res}'
        if days > 0:
            res = f'{days}天{res}'
        return res

    @staticmethod
    def get_cpu_info() -> dict:
        """获取CPU信息"""
        res = {'cpu_num': psutil.cpu_count(logical=True)}
        cpu_times = psutil.cpu_times()
        total = cpu_times.user + cpu_times.nice + cpu_times.system + cpu_times.idle \
                + get_attr(cpu_times, 'iowait', 0.0) + get_attr(cpu_times, 'irq', 0.0) \
                + get_attr(cpu_times, 'softirq', 0.0) + get_attr(cpu_times, 'steal', 0.0)
        res['total'] = round(total, 2)
        res['sys'] = round(cpu_times.system / total, 2)
        res['used'] = round(cpu_times.user / total, 2)
        res['wait'] = round(get_attr(cpu_times, 'iowait', 0.0) / total, 2)
        res['free'] = round(cpu_times.idle / total, 2)
        return res

    @staticmethod
    def get_mem_info() -> dict:
        """获取内存信息"""
        number = 1024 ** 3
        return {
            'total': round(psutil.virtual_memory().total / number, 2),
            'used': round(psutil.virtual_memory().used / number, 2),
            'free': round(psutil.virtual_memory().available / number, 2),
            'usage': round(psutil.virtual_memory().percent, 2)}

    @staticmethod
    def get_sys_info() -> dict:
        """获取服务器信息"""
        return {
            'computerName': IpUtil.get_host_name(),
            'computerIp': IpUtil.get_host_ip(),
            'userDir': os.path.dirname(os.path.abspath(os.path.join(__file__, '../..'))),
            'osName': platform.system(),
            'osArch': platform.machine()}

    @staticmethod
    def get_disk_info() -> List[dict]:
        """获取磁盘信息"""
        disk_info = []
        for disk in psutil.disk_partitions():
            usage = psutil.disk_usage(disk.mountpoint)
            disk_info.append({
                'dirName': disk.mountpoint,
                'sysTypeName': disk.fstype,
                'typeName': disk.device,
                'total': ServerInfo.get_size(usage.total),
                'free': ServerInfo.get_size(usage.free),
                'used': ServerInfo.get_size(usage.used),
                'usage': round(usage.percent, 2),
            })
        return disk_info

    @staticmethod
    def get_py_info():
        """获取Python环境及服务信息"""
        number = 1024 ** 2
        cur_proc = psutil.Process(os.getpid())
        mem_info = cur_proc.memory_info()
        start_dt = datetime.fromtimestamp(cur_proc.create_time())
        return {
            'name': 'Python',
            'version': platform.python_version(),
            'home': sys.executable,
            'inputArgs': '[{}]'.format(', '.join(sys.argv[1:])),
            'total': round(mem_info.vms / number, 2),
            'max': round(mem_info.vms / number, 2),
            'free': round((mem_info.vms - mem_info.rss) / number, 2),
            'usage': round(mem_info.rss / number, 2),
            'runTime': ServerInfo.fmt_timedelta(datetime.now() - start_dt),
            'startTime': start_dt.strftime(ServerInfo.datetime_fmt),
        }
