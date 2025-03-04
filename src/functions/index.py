"""
根目录
"""
from flask import render_template
from src.functions.database.models import Post


def index_logic():
    posts = Post.query.filter_by(deleted=False).all()
    return render_template('index.html', posts=posts)