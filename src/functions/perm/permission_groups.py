"""
权限组
@Dev JasonHan

这个权限组的风格仿照PocketMine插件中的PurePerms，拥有高度的可自定义性和灵活性
支持从某个权限组中继承某个权限，或者继承全部的权限
以及支持规定某个权限组应当调用哪一个函数
支持从perm.py里修改权限组
"""
from src.functions.perm import perm
from flask import g, jsonify


def extend_permission(group_name: str) -> any:
    """
    权限组继承的装饰器工厂
    :param group_name: 权限组名称
    """
    merged_perm = merge_permissions(group_name)

    def decorator(func):
        def wrapper(*args, **kwargs):
            kwargs['perm'] = merged_perm
            return func(*args, **kwargs)

        return wrapper

    return decorator


def get_perm_status() -> dict:
    """
    获取完整的权限状态字典
    :return: 如 {'send_post': True, 'edit_post': False}
    """
    return perm.groups.copy()


def merge_permissions(group_name: str) -> dict:
    """
    递归合并权限组
    :param group_name: 目标权限组名称
    :return: 合并后的权限字典
    """

    def _merge(g_name, visited=None):
        visited = visited or set()
        if g_name in visited:
            raise ValueError(f"循环继承检测: {g_name}")
        visited.add(g_name)

        group = perm.groups.get(g_name, {})
        merged = {}

        # 合并父级权限
        if "extends" in group:
            parent_perms = _merge(group["extends"], visited.copy())
            merged.update(parent_perms)

        # 合并当前权限（覆盖父级）
        merged.update({k: v for k, v in group.items() if k != "extends"})
        return merged

    return _merge(group_name)


def permission_group_logic(user_id, group_name, operation):
    if g.user.id != user_id:
        return jsonify(success=False, message="Invalid Userid")

    merged_perm = merge_permissions(group_name)  # 关键修改：使用合并后的权限

    if operation in merged_perm:  # 检查合并后的权限字典
        return jsonify(success=merged_perm[operation],
                     message="Allowed" if merged_perm[operation] else "Forbidden")
    return jsonify(success=False, message="Undefined operation")
