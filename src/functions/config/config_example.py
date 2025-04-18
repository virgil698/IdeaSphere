import os
import yaml
import pytz


def generate_config_example():
    config_example_path = 'config_example.yml'

    # 获取所有时区名称
    all_timezones = pytz.all_timezones

    # 定义示例配置内容
    config_example_content = {
        'port': 5000,
        'debug': True,
        'timezone': 'UTC',
        'database': {
            'uri': 'sqlite:///forum.db',
            'track_modifications': False
        },
        'csrf': {
            'enabled': True,
            'ssl_strict': True
        },
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'password': ''
        },
        'timezones': {
            'common': [
                'UTC',
                'Asia/Shanghai',
                'Asia/Tokyo',
                'Asia/Seoul',
                'Europe/London',
                'Europe/Paris',
                'America/New_York',
                'America/Los_Angeles'
            ],
            'all': all_timezones
        }
    }

    # 定义注释内容
    comments = {
        'port': '# 释放端口，默认 http',
        'debug': '# debug 模式，默认开启',
        'timezone': '# 默认时区为 UTC，可以设置为其他时区（如 Asia/Shanghai）',
        'database': {
            'uri': '# 数据库地址',
            'track_modifications': '# 用于跟踪模型的修改，默认关闭（对性能有一定影响）'
        },
        'csrf': {
            'enabled': '# 默认开启',
            'ssl_strict': '# 默认开启'
        },
        'redis': {
            'host': '# Redis 服务器地址',
            'port': '# Redis 服务器端口',
            'db': '# Redis 数据库编号',
            'password': '# Redis 密码（如果需要）'
        },
        'timezones': {
            'common': '# 常用时区列表',
            'all': '# 完整时区列表（供参考）'
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

        # 添加 Redis 配置注释
        f.write("# Redis 配置\n")
        f.write("redis:\n")
        f.write(f"  host: '{config_example_content['redis']['host']}' {comments['redis']['host']}\n")
        f.write(f"  port: {config_example_content['redis']['port']} {comments['redis']['port']}\n")
        f.write(f"  db: {config_example_content['redis']['db']} {comments['redis']['db']}\n")
        f.write(f"  password: '{config_example_content['redis']['password']}' {comments['redis']['password']}\n\n")

        # 添加时区列表注释
        f.write("# 允许使用的时区列表\n")
        f.write("timezones:\n")
        f.write(f"  common: {config_example_content['timezones']['common']} {comments['timezones']['common']}\n")
        f.write(
            f"  all: {config_example_content['timezones']['all'][:10]} ... (完整列表见 https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) {comments['timezones']['all']}\n")

        # 添加注意事项
        f.write("\n# 注意事项\n")
        f.write("# 1. 请确保时区设置正确，否则程序将使用默认的 UTC 时区。\n")
        f.write("# 2. 如果需要修改数据库地址，请确保数据库服务已启动。\n")
        f.write("# 3. Redis 配置中的密码如果为空，请确保 Redis 服务未设置密码。\n")
        f.write("# 4. 请勿随意修改配置文件的结构，否则可能导致程序无法正常运行。\n")

    print(f"示例配置文件已生成: {config_example_path}")


if __name__ == '__main__':
    generate_config_example()