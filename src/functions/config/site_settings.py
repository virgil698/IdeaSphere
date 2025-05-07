import os
import yaml
from pathlib import Path

def load_site_settings():
    settings_path = Path("config/site_settings.yml")
    if not settings_path.exists():
        # 如果配置文件不存在，创建一个默认的
        default_settings = {
            "site_name": "IdeaSphere",
            "footer_enabled": False,  # 默认关闭页脚
            "maintenance_mode": False
        }
        os.makedirs(settings_path.parent, exist_ok=True)
        with open(settings_path, "w", encoding="utf-8") as f:
            yaml.dump(default_settings, f, allow_unicode=True)
        return default_settings
    else:
        with open(settings_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

def save_site_settings(settings):
    settings_path = Path("config/site_settings.yml")
    os.makedirs(settings_path.parent, exist_ok=True)
    with open(settings_path, "w", encoding="utf-8") as f:
        yaml.dump(settings, f, allow_unicode=True)

def get_footer_setting():
    settings = load_site_settings()
    return settings.get("footer_enabled", False)