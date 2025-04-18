import os
import yaml
from src.db_ext import db

def get_config():
    config_path = 'config.yml'
    if not os.path.exists(config_path):
        # 定义默认配置内容
        default_config_content = """# IdeaSphere 配置文件
# 开源地址：https://github.com/IdeaSphere-team/IdeaSphere

# 基础配置
port: 5000 # 释放端口，默认 http
debug: True # debug 模式，默认开启

# SQLite3 数据库相关（建议保持默认状态）
database:
  uri: 'sqlite:///forum.db' # 数据库地址
  track_modifications: False # 用于跟踪模型的修改，默认关闭（对性能有一定影响）

# CSRF 保护相关（建议保持默认开启）
csrf:
  enabled: True # 默认开启
  ssl_strict: True # 默认开启

# Redis 配置
redis:
  host: 'localhost'  # Redis 服务器地址
  port: 6379         # Redis 服务器端口
  db: 0             # Redis 数据库编号
  password: ''      # Redis 密码（如果需要）
"""
        # 使用 UTF-8 编码写入文件
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(default_config_content)
    else:
        # 使用 UTF-8 编码读取文件
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    # 解析默认配置内容
    return yaml.safe_load(default_config_content)

def initialize_database(app):
    with app.app_context():
        db.create_all()