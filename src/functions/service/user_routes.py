# src/functions/service/user_routes.py

from flask import Blueprint, render_template, request, jsonify
from src.functions.database.models import User, Post, Comment, Report, Like
from src.db_ext import db
from datetime import datetime
user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
def get_user_data(user_uid):
    user = User.query.filter_by(user_uid=user_uid).first()
    if not user:
        return None

    # 获取用户的基本信息
    user_data = {
        'id': user.id,
        'user_uid': user.user_uid,
        'username': user.username,
        'brief': f"用户 {user.username} 的个人空间",
        'location': "四川，中国",
        'birthday': "2021/03/12",
        'gender': "男",
        'today_online': "6 小时 17 分 33 秒",
        'bilibili': "https://space.bilibili.com/401319663",
        'github': "https://github.com/Virgi1698",
        'weibo': "https://weibo.com/u/123456789",
        'blog': "https://blog.beixibaobao.com/",
        'posts_count': Post.query.filter_by(author_id=user.id, deleted=False).count(),
        'following_count': 7,
        'followers_count': 49
    }

    # 获取用户的活动信息
    activity_data = []
    for post in Post.query.filter_by(author_id=user.id, deleted=False).order_by(Post.created_at.desc()).limit(10).all():
        activity_data.append({
            'id': post.id,
            'type': 'post',
            'title': post.title,
            'time': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    for comment in Comment.query.filter_by(author_id=user.id, deleted=False).order_by(Comment.created_at.desc()).limit(10).all():
        activity_data.append({
            'id': comment.id,
            'type': 'comment',
            'content': comment.content,
            'time': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    # 获取用户的点赞信息
    likes = Like.query.filter_by(user_id=user.id).all()
    like_data = []
    for like in likes:
        if like.post_id:
            post = Post.query.get(like.post_id)
            like_data.append({
                'id': post.id,
                'type': 'post',
                'title': post.title,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        elif like.comment_id:
            comment = Comment.query.get(like.comment_id)
            like_data.append({
                'id': comment.id,
                'type': 'comment',
                'content': comment.content,
                'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

    # 获取用户的投稿帖子
    posts = Post.query.filter_by(author_id=user.id, deleted=False).order_by(Post.created_at.desc()).all()
    post_data = []
    for post in posts:
        post_data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'time': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'like_count': post.like_count,
            'comment_count': Comment.query.filter_by(post_id=post.id, deleted=False).count(),
            'section': post.section  # 添加 section 信息
        })

    return {
        'user': user_data,
        'activities': activity_data,
        'likes': like_data,
        'posts': post_data
    }


@user_bp.route('/user/<int:user_uid>')
def profile(user_uid):
    user_data = get_user_data(user_uid)
    if not user_data:
        return jsonify({'error': '用户不存在'}), 404

    return render_template('user/user_profile.html', user=user_data['user'], activities=user_data['activities'],
                           likes=user_data['likes'], posts=user_data['posts'])


@user_bp.route('/user/<int:user_uid>/activity')
def activity(user_uid):
    user_data = get_user_data(user_uid)
    if not user_data:
        return jsonify({'error': '用户不存在'}), 404

    return render_template('user/user_activity.html', user=user_data['user'], activities=user_data['activities'])


@user_bp.route('/user/<int:user_uid>/activity-feed')
def activity_feed(user_uid):
    user_data = get_user_data(user_uid)
    if not user_data:
        return jsonify({'error': '用户不存在'}), 404

    return render_template('user/user_activity_feed.html', user=user_data['user'], activities=user_data['activities'])


@user_bp.route('/user/<int:user_uid>/posts')
def user_posts(user_uid):
    user_data = get_user_data(user_uid)
    if not user_data:
        return jsonify({'error': '用户不存在'}), 404

    return render_template('user/user_posts.html', user=user_data['user'], posts=user_data['posts'])


@user_bp.route('/user/<int:user_uid>/treeholes')
def user_treeholes(user_uid):
    user_data = get_user_data(user_uid)
    if not user_data:
        return jsonify({'error': '用户不存在'}), 404
    return render_template('user/user_treeholes.html', user=user_data['user'])