"""
获取系统占用
"""
import psutil
import platform
from flask import jsonify
import cpuinfo

class SystemMonitor:
    """
    获取CPU占用的百分比
    """

    @classmethod
    def get_cpu_usage_percent(cls):
        return jsonify({
            "success": True,
            "cpu_usage": InitMonitor()._process.cpu_percent(interval=None)
        })

    """
    获取内存占用的百分比
    """

    @classmethod
    def get_memory_usage(cls):
        return jsonify({
            "success": True,
            "memory_usage": InitMonitor()._process.memory_percent()
        })

    """
    获取实际的物理占用
    For Memory
    """

    @classmethod
    def get_real_physics_usage(cls):
        return jsonify({
            "success": True,
            "physics_memory_total": int(InitMonitor()._memory_process.total / 1024000000),
            "available": int(InitMonitor()._memory_process.available / 1024000000),
            "percent": InitMonitor()._memory_process.percent,
            "used": int(InitMonitor()._memory_process.used / 1024000000),
            "free": int(InitMonitor()._memory_process.free / 1024000000),
            "active": int(InitMonitor()._memory_process.active / 1024000000) if hasattr(InitMonitor()._memory_process, 'active') else 0,
            "inactive": int(InitMonitor()._memory_process.inactive / 1024000000) if hasattr(InitMonitor()._memory_process, 'inactive') else 0,
            "wired": int(InitMonitor()._memory_process.wired / 1024000000) if hasattr(InitMonitor()._memory_process, 'wired') else 0,
        })

    """
    获取主机基本信息
    """
    @classmethod
    def get_basic_info_for_machine(cls):
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


class InitMonitor:
    _process = psutil.Process()
    _process.cpu_percent(interval=None)
    _process.memory_percent()
    _memory_process = psutil.virtual_memory()
    _logic_count = psutil.cpu_count()
    _physics_count = psutil.cpu_count(logical=False)
    _disk_part_info = psutil.disk_partitions()

    # 使用 platform.uname() 替代 os.uname()
    _system_info = platform.uname()
    _system_name = f"{_system_info.system}-{_system_info.release}-{_system_info.version}"

    # 根据系统类型设置系统名称
    _os = None
    if _system_info.system == 'Linux':
        _os = 'Linux'
    elif _system_info.system == 'Windows':
        _os = 'Windows'
    elif _system_info.system == 'Darwin':
        _os = 'MacOS'
    else:
        _os = 'Unknown System'

    _cpu_info = platform.processor()
    _cpu_model = cpuinfo.get_cpu_info().get('brand_raw', 'Unknown CPU')

    # 获取磁盘使用情况
    _disk_usage_info = {}
    for partition in _disk_part_info:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            _disk_usage_info[partition.device] = {
                'total': int(usage.total / 1024000000),
                'used': int(usage.used / 1024000000),
                'free': int(usage.free / 1024000000),
                'percent': usage.percent
            }
        except PermissionError:
            continue

    # 获取磁盘 I/O 信息
    _disk_io_info = psutil.disk_io_counters(perdisk=True)
    _disk_io_read_info = {disk: info.read_count for disk, info in _disk_io_info.items()}
    _disk_io_write_info = {disk: info.write_count for disk, info in _disk_io_info.items()}

    # 获取磁盘可用空间
    _disk_usage_info_available = {}
    for partition in _disk_part_info:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            _disk_usage_info_available[partition.device] = {
                'available': int(usage.free / 1024000000)
            }
        except PermissionError:
            continue