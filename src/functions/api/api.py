from flask import Blueprint, request, jsonify, abort, g
from src.functions.database.models import db, Report, Like, Post, Comment, User
from src.functions.parser.markdown_parser import convert_markdown_to_html
from flask_wtf.csrf import CSRFProtect
import datetime

csrf = CSRFProtect()

api_bp = Blueprint('api', __name__)

def get_csrf_token():
    return request.headers.get('X-CSRFToken')

@api_bp.before_request
def validate_csrf():
    if request.method in ['POST', 'PUT', 'DELETE']:
        csrf_token = get_csrf_token()
        if not csrf_token:
            abort(400, description='Missing CSRF Token')
        # 这里可以添加 CSRF Token 的验证逻辑
        # 例如，从数据库或缓存中验证 Token 的有效性

@api_bp.route('/handle_report/<int:report_id>', methods=['POST'])
def handle_report(report_id):
    status = request.json.get('status')
    if status not in ['valid', 'invalid']:
        return jsonify({'success': False, 'message': '无效的状态值'})

    report = db.session.get(Report, report_id)
    if not report:
        abort(404)

    if status == 'valid':
        if report.post:
            report.post.deleted = True
            report.post.delete_reason = report.reason
            report.post.delete_time = datetime.datetime.now()
        elif report.comment:
            report.comment.deleted = True
            report.comment.delete_reason = report.reason
            report.comment.delete_time = datetime.datetime.now()
        report.status = 'closed'
        report.resolved_by = g.user.id
    elif status == 'invalid':
        report.status = 'closed'
        report.resolved_by = g.user.id

    db.session.commit()
    return jsonify({'success': True, 'message': '举报已处理'})

@api_bp.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
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

@api_bp.route('/like_comment/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
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

@api_bp.route('/report_post/<int:post_id>', methods=['POST'])
def report_post(post_id):
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

@api_bp.route('/report_comment/<int:comment_id>', methods=['POST'])
def report_comment(comment_id):
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

@api_bp.route('/create_comment/<int:post_id>', methods=['POST'])
def create_comment(post_id):
    if not g.user:
        return jsonify({'success': False, 'message': '未登录'})

    # 验证 CSRF Token
    csrf_token = get_csrf_token()
    if not csrf_token:
        abort(400, description='Missing CSRF Token')

    content = request.json.get('content', '')
    if not content:
        return jsonify({'success': False, 'message': '评论内容不能为空'})

    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    html_content = convert_markdown_to_html(content)
    new_comment = Comment(
        content=content,
        html_content=html_content,
        author_id=g.user.id,
        post_id=post.id
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'success': True, 'message': '评论添加成功！'})