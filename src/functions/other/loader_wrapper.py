# 在 loader_wrapper.py 中添加逻辑
from src.functions.config.site_settings import get_loader_setting

def should_show_loader():
    return get_loader_setting()