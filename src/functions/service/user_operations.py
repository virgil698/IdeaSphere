from datetime import datetime

from flask import g, jsonify, request, abort, flash, url_for, redirect, render_template

from src.functions.database.models import Report, db, Like, Post, Comment, User, ReplyComment
from src.functions.parser.markdown_parser import convert_markdown_to_html


def like_post_logic(post_id):
    if not g.user:
        return jsonify({'success': False, 'message': '未登录'})

    existing_like = Like.query.filter_by(user_id=g.user.id, post_id=post_id).first()
    if existing_like:
        return jsonify({'success': False, 'message': '您已经点过赞了'})

    new_like = Like(user_id=g.user.id, post_id=post_id)
    db.session.add(new_like)
    db.session.query(Post).filter_by(id=post_id).update({'like_count': Post.like_count + 1})
    db.session.commit()

    post = db.session.get(Post, post_id)
    return jsonify({'success': True, 'like_count': post.like_count})


def like_comment_logic(comment_id):
    if not g.user:
        return jsonify({'success': False, 'message': '未登录'})

    existing_like = Like.query.filter_by(user_id=g.user.id, comment_id=comment_id).first()
    if existing_like:
        return jsonify({'success': False, 'message': '您已经点过赞了'})

    new_like = Like(user_id=g.user.id, comment_id=comment_id)
    db.session.add(new_like)
    db.session.query(Comment).filter_by(id=comment_id).update({'like_count': Comment.like_count + 1})
    db.session.commit()

    comment = db.session.get(Comment, comment_id)
    return jsonify({'success': True, 'like_count': comment.like_count})


def upgrade_user_logic(user_id):
    if g.role != 'admin':
        abort(403)

    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    user.role = 'moderator'
    db.session.commit()
    flash('用户已提升为版主', 'success')
    return redirect(url_for('manage_users'))


def downgrade_user_logic(user_id):
    if g.role != 'admin':
        abort(403)

    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    user.role = 'user'
    db.session.commit()
    flash('版主已降级为普通用户', 'success')
    return redirect(url_for('manage_users'))


def edit_post_logic(post_id):
    if g.role not in ['admin', 'moderator']:
        abort(403)
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.html_content = convert_markdown_to_html(post.content)
        db.session.commit()
        flash('帖子编辑成功！', 'success')
        return redirect(url_for('manage_posts'))

    return render_template('post/edit_post.html', post=post)


def follow_user_logic(follower_id, following_id):
    if not g.user:
        return jsonify({'success': False, 'message': '未登录'})

    # 检查是否已经关注
    existing_follow = g.user.following.filter_by(following_id=following_id).first()
    if existing_follow:
        return jsonify({'success': False, 'message': '您已经关注过此用户'})

    # 添加关注关系
    g.user.following.append(User(id=following_id))
    db.session.commit()

    return jsonify({'success': True, 'message': '关注成功'})


def unfollow_user_logic(follower_id, following_id):
    if not g.user:
        return jsonify({'success': False, 'message': '未登录'})

    # 检查是否已经关注
    existing_follow = g.user.following.filter_by(following_id=following_id).first()
    if not existing_follow:
        return jsonify({'success': False, 'message': '您没有关注此用户'})

    # 移除关注关系
    g.user.following.remove(existing_follow)
    db.session.commit()

    return jsonify({'success': True, 'message': '取消关注成功'})


def get_following_logic(user_id):
    following_users = User.query.filter(User.followers.any(follower_id=user_id)).all()
    following_list = [{'id': user.id, 'username': user.username} for user in following_users]
    return jsonify({'success': True, 'following': following_list})


def get_followers_logic(user_id):
    fan_users = User.query.filter(User.following.any(following_id=user_id)).all()
    followers_list = [{'id': user.id, 'username': user.username} for user in fan_users]
    return jsonify({'success': True, 'followers': followers_list})


def reply_logic(comment_id, reply_content):
    if not g.user:
        return jsonify({'success': False, 'message': '未登录'})

    # 检查评论是否存在
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({'success': False, 'message': '评论不存在'})

    # 检查回复内容是否为空
    if not reply_content:
        return jsonify({'success': False, 'message': '回复内容不能为空'})

    # 创建回复
    new_reply = ReplyComment(
        reply_message=reply_content,
        reply_user=g.user.username,
        target_comment_id=comment_id
    )
    db.session.add(new_reply)
    db.session.commit()

    return jsonify({'success': True, 'message': '回复成功'})