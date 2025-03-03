"""
权限组
@Dev JasonHan

这个权限组的风格仿照PocketMine插件中的PurePerms，拥有高度的可自定义性和灵活性
支持从某个权限组中继承某个权限，或者继承全部的权限
以及支持规定某个权限组应当调用哪一个函数
支持从perm.py里修改权限组
"""

import perm

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

# 使用继承链：admin → moderator → base
@extend_permission("admin")
def check_admin_perm(action: str, **kwargs) -> bool:
    return kwargs['perm'].get(action, False)

print(check_admin_perm("send_post"))   # 输出 True（继承自base）
print(check_admin_perm("delete_post")) # 输出 True（继承自moderator）
print(check_admin_perm("manage_users"))# 输出 True（自身权限）

def show_inherited_perms(group_name: str) -> dict:
    """显示指定权限组的完整继承结果"""
    return merge_permissions(group_name)

# 查看admin组的最终权限
print(show_inherited_perms("admin"))
# 输出：{'send_post': True, 'edit_post': False, 'delete_post': True, 'manage_users': True}
