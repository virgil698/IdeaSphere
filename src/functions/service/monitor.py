"""
获取系统占用
"""
import psutil
from flask import jsonify


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
            "memory_usage": int(InitMonitor()._process.memory_percent())
        })

    """
    获取实际的物理占用
    """

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


class InitMonitor():
    _process = psutil.Process()
    _process.cpu_percent(interval=None)
    _process.memory_percent()
    _memory_process = psutil.virtual_memory()
