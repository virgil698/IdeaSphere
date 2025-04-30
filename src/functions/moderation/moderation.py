# src/functions/moderation/moderation.py

from datetime import datetime

from flask import Blueprint, g, jsonify, request, abort, render_template

from src.functions.database.models import Report, db

moderation_bp = Blueprint('moderation', __name__)

@moderation_bp.route('/moderation')
def moderation_panel():
    return render_template('moderation/moderation_panel.html')

@moderation_bp.route('/reports/pending')
def moderation_reports_pending():
    reports = Report.query.filter_by(status='pending').all()
    pagination_pages = [1, 2, 3, 4, 5]  # 示例分页数据
    current_page = 1  # 示例当前页码
    return render_template('moderation/moderation_reports_pending.html', pending_reports=reports, pagination_pages=pagination_pages, current_page=current_page)

@moderation_bp.route('/reports/processed')
def moderation_reports_processed():
    reports = Report.query.filter(Report.status != 'pending').all()
    pagination_pages = [1, 2, 3, 4, 5]  # 示例分页数据
    current_page = 1  # 示例当前页码
    return render_template('moderation/moderation_reports_processed.html', processed_reports=reports, pagination_pages=pagination_pages, current_page=current_page)

@moderation_bp.route('/handle_report/<int:report_id>', methods=['POST'])
def handle_report(report_id):
    if g.role not in ['admin', 'moderator']:
        abort(403)
    report = Report.query.get(report_id)
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
        report.resolved_by = g.user.id if g.user else None
        db.session.commit()
        return jsonify({'success': True, 'message': '已违规，内容已隐藏'})
    elif status == 'invalid':
        report.status = 'closed'
        report.resolved_by = g.user.id if g.user else None
        db.session.commit()
        return jsonify({'success': True, 'message': '未违规，举报已关闭'})