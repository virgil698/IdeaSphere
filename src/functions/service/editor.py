"""
编辑器
"""
import os
from pathlib import Path
from flask import jsonify, request
import logging

class editor_tool:
    def __init__(self):
        self.path = Path(__file__).parent.parent.parent.parent
        # 定义允许的文件目录（可选）
        self.allowed_dir = os.path.join(self.path, 'allowed_directory')  # 替换为实际允许的目录

    def directory_tree(self):
        """生成包含目录和文件结构的嵌套字典（自动跳过无权限目录）"""

        def safe_get_tree(path: Path):
            try:
                tree = {
                    "name": path.name,
                    "type": "directory" if path.is_dir() else "file",
                    "children": []
                }
                if path.is_dir():
                    for item in path.iterdir():
                        try:
                            tree["children"].append(safe_get_tree(item))
                        except PermissionError as e:
                            logging.warning(f"Skipped {item}: {str(e)}")
                            continue
                return tree
            except PermissionError as e:
                logging.error(f"Access denied: {path}")
                raise  # 抛出异常给外层处理

        try:
            return jsonify({
                "success": True,
                "tree": safe_get_tree(self.path.resolve())
            })
        except PermissionError as e:
            return jsonify({
                "success": False,
                "error": f"Permission denied: {str(e)}",
                "path": str(self.path.resolve())
            })

    def get_file_content(self):
        filename = request.json.get('filename')

        # 新增扩展名过滤
        if Path(filename).suffix in ['.pyc', '.exe', '.so']:  # 添加需要排除的二进制扩展名
            return jsonify({
                "success": False,
                "error": "Binary files cannot be read"
            })

        # 验证文件路径是否在允许的目录内
        if not self.is_safe_path(filename):
            return jsonify({
                "success": False,
                "error": "Invalid file path"
            })

        for dirpath, _, filenames in os.walk(self.path):
            if filename in filenames:
                file_path = Path(dirpath) / filename
                try:
                    # 使用二进制模式读取 + 自动编码检测
                    with open(file_path, 'rb') as f:  # 改为二进制模式
                        raw_data = f.read()
                        try:
                            content = raw_data.decode('utf-8')
                        except UnicodeDecodeError:
                            # 尝试其他编码（如GBK）
                            content = raw_data.decode('gbk', errors='replace')

                    return jsonify({
                        "success": True,
                        "content": content
                    })
                except Exception as e:  # 更广泛的异常捕获
                    logging.error(f"Read {file_path} failed: {str(e)}")
                    return jsonify({
                        "success": False,
                        "error": f"Read failed: {str(e)}"
                    })

        return jsonify({"success": False, "error": "File not found"})

    def save_file(self):
        contents = request.json.get('content')
        filename = request.json.get('filename')

        # 验证文件路径是否在允许的目录内
        if not self.is_safe_path(filename):
            return jsonify({
                "success": False,
                "error": "Invalid file path"
            })

        # 限制文件保存路径到指定目录
        safe_file_path = os.path.join(self.allowed_dir, os.path.basename(filename))
        try:
            with open(safe_file_path, 'w') as f:
                f.write(contents)
            return jsonify({"success": True})
        except Exception as e:
            logging.error(f"Save {safe_file_path} failed: {str(e)}")
            return jsonify({
                "success": False,
                "error": f"Save failed: {str(e)}"
            })

    def is_safe_path(self, filename):
        """验证文件路径是否安全"""
        # 确保文件名中不包含路径穿越元素
        if '..' in filename or filename.startswith('/'):
            return False

        # 确保文件路径在允许的目录范围内
        allowed_dir = os.path.abspath(self.allowed_dir)
        file_path = os.path.abspath(os.path.join(self.path, filename))
        if not file_path.startswith(allowed_dir):
            return False

        return True