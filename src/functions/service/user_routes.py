# src/functions/service/user_routes.py

from datetime import datetime, timedelta

from flask import Blueprint, render_template, jsonify
from sqlalchemy import func

from src.db_ext import db
from src.functions.database.models import User, Post, Comment, Report, Like, UserContribution, ReplyComment

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


@user_bp.route('/user/<int:user_uid>/contributions')
def get_user_contributions(user_uid):
    # 获取用户过去70天的贡献数据
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=69)

    contributions = UserContribution.query.filter(
        UserContribution.user_uid == user_uid,
        UserContribution.date.between(start_date, end_date)
    ).all()

    # 格式化数据
    contributions_data = {}
    for contribution in contributions:
        contributions_data[contribution.date.isoformat()] = contribution.contribution_value

    # 补全缺失的日期（贡献值为0）
    current_date = start_date
    while current_date <= end_date:
        if current_date.isoformat() not in contributions_data:
            contributions_data[current_date.isoformat()] = 0
        current_date += timedelta(days=1)

    return jsonify(contributions_data)


def calculate_contributions(user_uid):
    user = User.query.filter_by(user_uid=user_uid).first()
    if not user:
        return None

    # 获取用户过去70天的活动数据
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=69)

    # 删除旧的贡献记录（保留最近70天）
    UserContribution.query.filter(
        UserContribution.user_uid == user_uid,
        UserContribution.date < start_date
    ).delete()
    db.session.commit()

    current_date = start_date
    while current_date <= end_date:
        # 计算当天的活动数（帖子、评论、回复、点赞、举报）
        posts_count = Post.query.filter(
            Post.author_id == user.id,
            func.date(Post.created_at) == current_date
        ).count()

        comments_count = Comment.query.filter(
            Comment.author_id == user.id,
            func.date(Comment.created_at) == current_date
        ).count()

        reply_count = ReplyComment.query.filter(
            func.date(ReplyComment.reply_at) == current_date
        ).count()

        like_count = Like.query.filter(
            Like.user_id == user.id,
            func.date(Like.created_at) == current_date
        ).count()

        report_count = Report.query.filter(
            Report.user_id == user.id,
            func.date(Report.created_at) == current_date
        ).count()

        # 总贡献值（每个活动算1点）
        total_contribution = posts_count + comments_count + reply_count + like_count + report_count

        # 新用户注册当天贡献为20
        if current_date == user.created_at.date():
            total_contribution = 20

        # 添加或更新贡献记录
        existing_contribution = UserContribution.query.filter_by(
            user_uid=user_uid,
            date=current_date
        ).first()

        if existing_contribution:
            existing_contribution.contribution_value = total_contribution
        else:
            new_contribution = UserContribution(
                user_uid=user_uid,
                date=current_date,
                contribution_value=total_contribution
            )
            db.session.add(new_contribution)

        current_date += timedelta(days=1)

    db.session.commit()
    return {'message': 'Contributions calculated and updated successfully'}