import yaml
import pytz
import os

def ensure_config_directory():
    config_dir = 'config'
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return config_dir

def generate_config_example():
    config_dir = ensure_config_directory()  # 确保 config 文件夹存在
    config_example_path = os.path.join(config_dir, 'config_example.yml')

    # 获取所有时区名称
    all_timezones = pytz.all_timezones

    # 定义示例配置内容
    config_example_content = {
        'port': 5000,
        'debug': True,
        'paths': {
            'templates': 'templates',
            'static': 'static'
        },
        'timezone': 'UTC',
        'database': {
            'uri': 'sqlite:///forum.db',
            'track_modifications': False
        },
        'csrf': {
            'enabled': True,
            'ssl_strict': True
        }
    }

    # 定义注释内容
    comments = {
        'port': '# 释放端口，默认 http',
        'debug': '# debug 模式，默认开启',
        'paths': {
            'templates': '# 模板文件夹路径',
            'static': '# 静态文件夹路径'
        },
        'timezone': '# 默认时区为 UTC，可以设置为其他时区（如 Asia/Shanghai）',
        'database': {
            'uri': '# 数据库地址',
            'track_modifications': '# 用于跟踪模型的修改，默认关闭（对性能有一定影响）'
        },
        'csrf': {
            'enabled': '# 默认开启',
            'ssl_strict': '# 默认开启'
        }
    }

    # 使用 UTF-8 编码写入文件
    with open(config_example_path, 'w', encoding='utf-8') as f:
        # 添加文件头部注释
        f.write("# IdeaSphere 示例配置文件\n")
        f.write("# 开源地址：https://github.com/IdeaSphere-team/IdeaSphere\n\n")

        # 添加基础配置注释
        f.write("# 基础配置\n")
        f.write(f"port: {config_example_content['port']} {comments['port']}\n")
        f.write(f"debug: {config_example_content['debug']} {comments['debug']}\n\n")

        # 添加路径配置注释
        f.write("# 路径配置\n")
        f.write("paths:\n")
        f.write(f"  templates: '{config_example_content['paths']['templates']}' {comments['paths']['templates']}\n")
        f.write(f"  static: '{config_example_content['paths']['static']}' {comments['paths']['static']}\n\n")

        # 添加时区配置注释
        f.write("# 时区配置\n")
        f.write(f"timezone: '{config_example_content['timezone']}' {comments['timezone']}\n\n")

        # 添加数据库配置注释
        f.write("# SQLite3 数据库相关（建议保持默认状态）\n")
        f.write("database:\n")
        f.write(f"  uri: '{config_example_content['database']['uri']}' {comments['database']['uri']}\n")
        f.write(
            f"  track_modifications: {config_example_content['database']['track_modifications']} {comments['database']['track_modifications']}\n\n")

        # 添加 CSRF 配置注释
        f.write("# CSRF 保护相关（建议保持默认开启）\n")
        f.write("csrf:\n")
        f.write(f"  enabled: {config_example_content['csrf']['enabled']} {comments['csrf']['enabled']}\n")
        f.write(f"  ssl_strict: {config_example_content['csrf']['ssl_strict']} {comments['csrf']['ssl_strict']}\n\n")

    print(f"示例配置文件已生成: {config_example_path}")

if __name__ == '__main__':
    generate_config_example()