"""
权限组
@Dev JasonHan

这个权限组的风格仿照PocketMine插件中的PurePerms，拥有高度的可自定义性和灵活性
支持从某个权限组中继承某个权限，或者继承全部的权限
以及支持规定某个权限组应当调用哪一个函数
支持从perm.yml里修改权限组
"""
import os.path

import yaml


def extend_permission(perm) -> any:
    """
    继承 -- Extend Function
    这是一个工厂函数
    Dev:
       Dev: JasonHan
    :returns:
        result (any)
        extends_wrapper (any)
        extends (any)
    param:
        perm (dict)
    """

    def extends(func):
        def extends_wrapper(*args, **kwargs):
            kwargs['perm'] = perm  # 将 perm 添加到 kwargs 中
            result = func(*args, **kwargs)
            return result
        return extends_wrapper
    return extends


"""
基本权限字典
@Dev Jason
啥也不return
(憋笑)
"""
base_dict = {
    # 用户类型权限
    "send_post": "enabled",
    "send_comment": "enabled",
    "allow_register": "enabled",
    "allow_login": "enabled",
    "allow_logout": "enabled",
    "allow_create_post": "enabled",
    "allow_repost_post": "enabled",
    "allow_delete_post": "enabled",
    "allow_send_comment": "enabled",
    "allow_like_post": "enabled",
    # 帖子权限
    "post_perm_dict": {
        # 允许别人看到这篇帖子
        "allow_somebody_see_this_post": "enabled"
    }
}


"""
基础权限组词典
"""
basic_perm_dict = {
    "base_dict.send_post": "enabled",
    "base_dict.send_comment": "enabled",
    "base_dict.allow_register": "enabled",
    "base_dict.allow_login": "enabled",
    "base_dict.allow_logout": "enabled",
    "base_dict.allow_create_post": "enabled",
    "base_dict.allow_repost_post": "enabled",
    "base_dict.allow_send_comment": "enabled",
    "base_dict.allow_like_post": "enabled",
}

def read_perm_from_yaml() -> any:
    """
    从perm.yml读取
    Dev:
       Dev: JasonHan
    :return:
        perm_yaml (any)
    """
    if not os.path.exists("perm.yml"):
        with open("perm.yml", "w") as f:
            yaml.dump("", f)
    with open("perm.yml", "r") as f:
        perm_yaml = yaml.safe_load(f)
    if perm_yaml is None:
        perm_yaml = {}
    return perm_yaml

def parse_basic_perm_data() -> dict:
    """
    从获取到的数据中解析基础权限组
    :return: (dict)
    """
    perm_yaml = read_perm_from_yaml()
    # 向内部添加一个基本权限组
    if 'basic' not in perm_yaml:
        perm_yaml['basic'] = basic_perm_dict  # 如果 'basic' 键不存在，使用 basic_perm_dict 初始化
        with open("perm.yml", "w") as f:
            yaml.dump(perm_yaml, f)
    return perm_yaml

def get_perm_dict() -> dict:
    """
    获取你自定义的权限组
    :return: perm_list(dict)
    """
    perm_yaml = parse_basic_perm_data()
    for key, value in perm_yaml.items():
        return {
            key : value
        }

def parser() -> dict:
    """
    权限组解析器
    :return: 解析后的权限组字典 (dict)
    """
    perm_dict = get_perm_dict()
    parsed_perm_dict = {}

    def merge_permissions(target, source):
        """递归合并两个权限字典"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                merge_permissions(target[key], value)
            else:
                target[key] = value

    for group_name, group_perms in perm_dict.items():
        extended_group = group_perms.get('extend')
        if extended_group:
            # 合并继承的权限组
            if extended_group in parsed_perm_dict:
                extended_perms = parsed_perm_dict[extended_group]
            else:
                extended_perms = perm_dict.get(extended_group, {})
            # 更新当前权限组的权限
            merge_permissions(group_perms, extended_perms)
            # 移除 'extend' 键，因为它已经处理过了
            group_perms.pop('extend', None)
        parsed_perm_dict[group_name] = group_perms

    return parsed_perm_dict