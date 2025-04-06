"""
根目录
"""
from flask import render_template, request
from src.functions.database.models import Post

def index_logic():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    sort = request.args.get('sort', 'global')  # 默认按全局排序

    # 查询帖子并分页
    if sort == 'timeline':
        # 按时间线排序（最先发布的在前）
        posts = Post.query.filter_by(deleted=False).order_by(Post.created_at.asc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    else:
        # 按全局排序（默认排序）
        posts = Post.query.filter_by(deleted=False).order_by(Post.created_at.desc()).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    return render_template('index.html', posts=posts, pagination=posts)