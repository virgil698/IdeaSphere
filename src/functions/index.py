"""
根目录
"""
from flask import render_template, request, redirect, url_for
from src.functions.database.models import Post

def index_logic():
    return redirect(url_for('newest'))  # 默认重定向到时间线排序页面

def newest_logic():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 按时间线排序（最先发布的在前）
    posts = Post.query.filter_by(deleted=False).order_by(
        Post.created_at.desc()  # 按发布时间升序
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('index.html', posts=posts, sort='timeline')

def global_logic():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 按点赞数量排序（点赞最多的在前）
    posts = Post.query.filter_by(deleted=False).order_by(
        Post.like_count.desc(),  # 按点赞数量降序
        Post.created_at.desc()   # 点赞数量相同的情况下按时间降序
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('index.html', posts=posts, sort='global')