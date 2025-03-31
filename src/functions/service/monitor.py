"""
获取系统占用
"""
import psutil
import platform
from flask import jsonify
import cpuinfo
import os

class SystemMonitor:
    """
    获取CPU占用的百分比
    """

    @classmethod
    def get_cpu_usage_percent(self):
        return jsonify({
            "success": True,
            "cpu_usage": InitMonitor()._process.cpu_percent(interval=None)
        })

    """
    获取内存占用的百分比
    """

    @classmethod
    def get_memory_usage(self):
        return jsonify({
            "success": True,
            "memory_usage": InitMonitor()._process.memory_percent()
        })

    """
    获取实际的物理占用
    For Memory
    """

    @classmethod
    def get_real_physics_usage(self):
        return jsonify({
            "success": True,
            "physics_memory_total": int(InitMonitor()._memory_process[0] / 1024000000),
            "available": int(InitMonitor()._memory_process[1] / 1024000000),
            "percent": InitMonitor()._memory_process[2],
            "used": int(InitMonitor()._memory_process[3] / 1024000000),
            "free": int(InitMonitor()._memory_process[4] / 1024000000),
            "active": int(InitMonitor()._memory_process[5] / 1024000000),
            "inactive": int(InitMonitor()._memory_process[6] / 1024000000),
            "wired": int(InitMonitor()._memory_process[7] / 1024000000),
        })

    """
    获取主机基本信息
    """
    @classmethod
    def get_basic_info_for_machine(self):
        return jsonify({
            "success": True,
            "cpu_logic_count": InitMonitor()._logic_count,
            "cpu_physics_cores_count": InitMonitor()._physics_count,
            "disk_part_info": InitMonitor()._disk_part_info,
            "disk_usage_info": InitMonitor()._disk_usage_info,
            "disk_io_read_info": InitMonitor()._disk_io_read_info,
            "cpu_platform": InitMonitor()._cpu_info,
            "os_name": InitMonitor()._system_name,
            "os_type": InitMonitor()._os,
            'cpu_model': InitMonitor()._cpu_model,
            'disk_io_write_info': InitMonitor()._disk_io_write_info,
            'disk_usage_info_available': InitMonitor()._disk_usage_info_available
        })


class InitMonitor():
    _process = psutil.Process()
    _process.cpu_percent(interval=None)
    _process.memory_percent()
    _memory_process = psutil.virtual_memory()
    _logic_count = psutil.cpu_count()
    _physics_count = psutil.cpu_count(logical=False)
    _disk_part_info = psutil.disk_partitions()
    _disk_usage_info = int(psutil.disk_usage('/').used / 1024000000)
    _disk_usage_info_available = int(psutil.disk_usage('/').free / 1024000000)

    _disk_io_read_info = psutil.disk_io_counters().read_count
    _disk_io_write_info = psutil.disk_io_counters().write_count
    _cpu_info = platform.processor()
    _cpu_model = cpuinfo.get_cpu_info()['brand_raw']
    _system_name = os.uname()
    _os = None
    if 'Linux' in _system_name:
        _os = 'Linux'
    elif 'Windows' in _system_name:
        _os = 'Windows'
    elif 'Darwin' in _system_name:
        _os = 'MacOS'
    else:
        _os = 'Unknown System'