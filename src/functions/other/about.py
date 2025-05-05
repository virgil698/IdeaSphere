# src/functions/other/about.py

from flask import Blueprint, render_template
from src.db_ext import db
from src.functions.database.models import User, Post, Comment, Like

about_bp = Blueprint('about', __name__, url_prefix='/about')


@about_bp.route('/')
def about_page():
    # 获取管理员和版主信息
    admins = User.query.filter_by(role='admin').all()
    moderators = User.query.filter_by(role='moderator').all()

    # 获取站点统计信息
    site_stats = {
        'topics': {
            'day': db.session.query(Post).filter(
                db.func.date(Post.created_at) == db.func.date(db.func.current_timestamp())).count(),
            'week': db.session.query(Post).filter(
                Post.created_at >= db.func.date(db.func.current_timestamp(), '-7 days')).count(),
            'month': db.session.query(Post).filter(
                Post.created_at >= db.func.date(db.func.current_timestamp(), '-30 days')).count(),
            'total': db.session.query(Post).count()
        },
        'posts': {
            'day': db.session.query(Comment).filter(
                db.func.date(Comment.created_at) == db.func.date(db.func.current_timestamp())).count(),
            'week': db.session.query(Comment).filter(
                Comment.created_at >= db.func.date(db.func.current_timestamp(), '-7 days')).count(),
            'month': db.session.query(Comment).filter(
                Comment.created_at >= db.func.date(db.func.current_timestamp(), '-30 days')).count(),
            'total': db.session.query(Comment).count()
        },
        'users': {
            'day': db.session.query(User).filter(
                db.func.date(User.created_at) == db.func.date(db.func.current_timestamp())).count(),
            'week': db.session.query(User).filter(
                User.created_at >= db.func.date(db.func.current_timestamp(), '-7 days')).count(),
            'month': db.session.query(User).filter(
                User.created_at >= db.func.date(db.func.current_timestamp(), '-30 days')).count(),
            'total': db.session.query(User).count()
        },
        'likes': {
            'day': db.session.query(Like).filter(
                db.func.date(Like.created_at) == db.func.date(db.func.current_timestamp())).count(),
            'week': db.session.query(Like).filter(
                Like.created_at >= db.func.date(db.func.current_timestamp(), '-7 days')).count(),
            'month': db.session.query(Like).filter(
                Like.created_at >= db.func.date(db.func.current_timestamp(), '-30 days')).count(),
            'total': db.session.query(Like).count()
        }
    }

    return render_template('other/about.html', admins=admins, moderators=moderators, site_stats=site_stats)