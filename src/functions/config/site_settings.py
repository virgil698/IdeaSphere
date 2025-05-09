import os
import yaml
from pathlib import Path

# 配置文件的默认注释信息
DEFAULT_COMMENTS = {
    "site_name": "网站名称 - 显示在页面标题和相关位置",
    "footer_enabled": "页脚启用状态 - 是否在页面底部显示页脚信息",
    "maintenance_mode": "维护模式 - 是否启用网站维护模式"
}


def load_site_settings():
    settings_path = Path("config/site_settings.yml")
    if not settings_path.exists():
        # 如果配置文件不存在，创建一个默认的带注释的配置文件
        default_settings = {
            "site_name": "IdeaSphere",
            "footer_enabled": False,  # 默认关闭页脚
            "maintenance_mode": False
        }

        os.makedirs(settings_path.parent, exist_ok=True)
        generate_commented_yaml(default_settings, settings_path)
        return default_settings
    else:
        with open(settings_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)


def save_site_settings(settings):
    settings_path = Path("config/site_settings.yml")
    os.makedirs(settings_path.parent, exist_ok=True)
    generate_commented_yaml(settings, settings_path)


def generate_commented_yaml(data, file_path):
    """生成带注释的 YAML 文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        # 添加文件头注释
        f.write("# 网站配置文件\n")
        f.write("# 编辑此文件以自定义网站行为\n")
        f.write("# 修改后需要重启服务才能生效\n\n")

        # 遍历数据并添加注释
        for key, value in data.items():
            comment = DEFAULT_COMMENTS.get(key)
            if comment:
                f.write(f"# {comment}\n")
            # 写入实际数据，保留原始注释
            line = f"{key}: {yaml.dump({key: value}, default_flow_style=False, allow_unicode=True, sort_keys=False).split(key + ': ')[1]}"
            f.write(line)
            # 如果原始值有行内注释，保留它
            if isinstance(value, (bool, int, float, str)) and "#" in str(value):
                f.write(f"  # {value.split('#')[1].strip()}")
            f.write("\n")
        f.write("\n")


def get_footer_setting():
    settings = load_site_settings()
    return settings.get("footer_enabled", False)