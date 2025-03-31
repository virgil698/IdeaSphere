"""
日志实现（多线程版）
@DEV JASON
"""
import os
import tarfile
import threading
import time
from datetime import datetime


class Logger(threading.Thread):
    write_lock = threading.Lock()  # 类级别线程锁

    def __init__(
            self,
            threadID: int,
            name: str,
            counter: int,
            msg: str,
            mode: str,
            module_name: str = '',
            log_path:str = ""
        ):
        super().__init__()
        now = datetime.now()
        self.path =now.strftime("%Y-%m-%d") + '.log'
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.msg = msg
        self.logpath = log_path
        self.mode = mode
        self.modulename = module_name
        self.ascii_color = {
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
        }

    def run(self):
        """ 线程主执行方法 """
        while self.counter > 0:
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.write_main_function(
                time=formatted_time,
                mode=self.mode,
                msg=self.msg,
                module_name=self.modulename
            )
            self.counter -= 1
            time.sleep(1)  # 每次写入间隔1秒

    def write_main_function(self, time: str, mode: str, msg: str, module_name: str):
        """ 线程安全的日志写入 """
        with self.write_lock:
            with open(self.logpath + '/' + self.path, 'a', encoding='utf-8') as f:
                log_content = f"[{time}][{mode}][{module_name}] {msg}\n" if module_name \
                    else f"[{time}][{mode}] {msg}\n"

                color_code = self.ascii_color.get("yellow", "") if mode == "warn" \
                    else self.ascii_color.get("green", "")
                print(f"{color_code}{log_content}\033[0m")

                f.write(log_content)
    def package(self, size:int):
        """
        统计LOGS文件夹大小，并打包成tar.gz
        :param size:byte
        :return:
        """
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.logpath):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # 跳过可能存在的符号链接
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
            if total_size > size:
               with tarfile.open(f"{self.logpath}/logs.tar.gz", "w:gz") as tar:
                    tar.add(self.logpath, arcname=os.path.basename(self.logpath))

