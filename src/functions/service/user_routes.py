# src/functions/service/user_routes.py

from datetime import datetime, timedelta

from flask import Blueprint, render_template, jsonify
from sqlalchemy import func

from src.db_ext import db
from src.functions.database.models import User, Post, Comment, Report, Like, UserContribution, ReplyComment
from src.functions.database.redis import RedisManager

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
        'role': user.role,
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


# 每10分钟和凌晨1点计算贡献的函数
def scheduled_calculate_contributions():
    # 获取所有用户UID
    users = User.query.all()
    for user in users:
        calculate_contributions(user.user_uid)

def calculate_contributions(user_uid):
    user = User.query.filter_by(user_uid=user_uid).first()
    if not user:
        return None

    # 获取用户在过去一年内的活动数据
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)

    # 删除旧的贡献记录
    UserContribution.query.filter_by(user_uid=user_uid).delete()
    db.session.commit()

    current_date = start_date
    while current_date <= end_date:
        # 计算当天的帖子数
        posts_count = Post.query.filter(
            Post.author_id == user.id,
            func.date(Post.created_at) == current_date
        ).count()

        # 计算当天的评论数
        comments_count = Comment.query.filter(
            Comment.author_id == user.id,
            func.date(Comment.created_at) == current_date
        ).count()

        # 计算当天的回复数
        reply_count = ReplyComment.query.filter(
            func.date(ReplyComment.reply_at) == current_date
        ).count()

        # 计算当天的举报数
        reports_count = Report.query.filter(
            Report.user_id == user.id,
            func.date(Report.created_at) == current_date
        ).count()

        # 计算总贡献值
        total_contribution = (posts_count * 1 +
                              comments_count * 0.5 +
                              reply_count * 0.5 +
                              reports_count * 1)

        # 添加到数据库
        new_contribution = UserContribution(
            user_uid=user_uid,
            date=current_date,
            contribution_value=total_contribution
        )
        db.session.add(new_contribution)

        current_date += timedelta(days=1)

    db.session.commit()
    return {'message': 'Contributions calculated and updated successfully'}


def get_contributions_from_db(user_uid):
    # 尝试从Redis获取数据
    redis_conn = RedisManager.get_connection(3)
    cache_key = f"user_contributions:{user_uid}"
    cached_data = redis_conn.hgetall(cache_key)

    if cached_data:
        # 缓存命中，返回缓存数据
        return cached_data

    # 查询过去一年的数据
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)

    contributions = UserContribution.query.filter(
        UserContribution.user_uid == user_uid,
        UserContribution.date.between(start_date, end_date)
    ).all()

    # 格式化数据
    result = {}
    for contribution in contributions:
        result[contribution.date.isoformat()] = contribution.contribution_value

    # 存入Redis缓存
    if result:
        for date_str, value in result.items():
            redis_conn.hset(cache_key, date_str, value)
        redis_conn.expire(cache_key, 86400 * 7)  # 缓存7天

    return result