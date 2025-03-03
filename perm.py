# perm.py 必须包含如下结构
groups = {
    "base": {
        "send_post": True
    },
    "moderator": {
        "extends": "base",
        "delete_post": True
    },
    "admin": {
        "extends": "moderator",
        "manage_users": True
    }
}
