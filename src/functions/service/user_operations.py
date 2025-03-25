from datetime import datetime

from flask import g, jsonify, request, abort, flash, url_for, redirect, render_template

from src.functions.database.models import Report, db, Like, Post, Comment, User
from src.functions.parser.markdown_parser import convert_markdown_to_html


def report_post_logic(post_id):
    if not g.user:
        return jsonify({'success': False, 'message': '请登录后再进行举报'})

    reason = request.json.get('reason', '')
    if not reason:
        return jsonify({'success': False, 'message': '举报原因不能为空'})

    existing_report = Report.query.filter_by(post_id=post_id, user_id=g.user.id).first()
    if existing_report:
        return jsonify({'success': False, 'message': '您已经举报过此帖子'})

    new_report = Report(post_id=post_id, user_id=g.user.id, reason=reason)
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'success': True, 'message': '举报成功！'})


def report_comment_logic(comment_id):
    if not g.user:
        return jsonify({'success': False, 'message': '请登录后再进行举报'})

    reason = request.json.get('reason', '')
    if not reason:
        return jsonify({'success': False, 'message': '举报原因不能为空'})

    existing_report = Report.query.filter_by(comment_id=comment_id, user_id=g.user.id).first()
    if existing_report:
        return jsonify({'success': False, 'message': '您已经举报过此评论'})

    new_report = Report(comment_id=comment_id, user_id=g.user.id, reason=reason)
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'success': True, 'message': '举报成功！'})


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


def handle_report_logic(report_id):
    if g.role not in ['admin', 'moderator']:
        abort(403)

    report = db.session.get(Report, report_id)
    if not report:
        abort(404)

    status = request.json.get('status')
    if status not in ['valid', 'invalid']:
        return jsonify({'success': False, 'message': '无效的状态值'})

    if status == 'valid':
        if report.post:
            report.post.deleted = True
            report.post.delete_reason = report.reason
            report.post.delete_time = datetime.now()
        elif report.comment:
            report.comment.deleted = True
            report.comment.delete_reason = report.reason
            report.comment.delete_time = datetime.now()
        report.status = 'closed'
        report.resolved_by = g.user.id
        db.session.commit()
        return jsonify({'success': True, 'message': '已违规，内容已隐藏'})
    elif status == 'invalid':
        report.status = 'closed'
        report.resolved_by = g.user.id
        db.session.commit()
        return jsonify({'success': True, 'message': '未违规，举报已关闭'})


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

    return render_template('edit_post.html', post=post)