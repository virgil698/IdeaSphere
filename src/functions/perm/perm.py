groups = {
    "base": {
        "send_post": True,
        "delete_post": True,
        "like_post": True,
        "send_comment": True,
        "search_in_website": True
    },
    "admin": {
        "extends": "base",
        "manage_posts": True,
        "manage_users": True,
        "manage_reports": True,
    },
    "moderator": {
        "extends": "admin",
        "manage_permissions": True,
        "manage_config": True,
        "manage_groups": True,
        "manage_database": True,
        "manage_category": True
    }

}
