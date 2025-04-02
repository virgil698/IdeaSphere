from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.db_ext import db
from src.functions.database.models import Section, Post, Comment, User
from src.functions.utils.logger import Logger
from datetime import datetime, timedelta
from sqlalchemy import func

# 创建蓝图
section_bp = Blueprint('section', __name__, url_prefix='/section')

# 获取所有板块
@section_bp.route('/')
def sections():
    sections = Section.query.all()
    return render_template('sections.html', sections=sections)

# 创建板块
@section_bp.route('/create', methods=['GET', 'POST'])
def create_section():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon')

        if not name:
            flash('板块名称不能为空', 'error')
            return redirect(url_for('section.create_section'))

        # 检查板块名称是否已存在
        existing_section = Section.query.filter_by(name=name).first()
        if existing_section:
            flash('该板块名称已存在', 'error')
            return redirect(url_for('section.create_section'))

        # 创建新板块
        new_section = Section(
            name=name,
            description=description,
            icon=icon,
            post_count=0,
            comment_count=0
        )

        db.session.add(new_section)
        db.session.commit()

        flash('板块创建成功', 'success')
        return redirect(url_for('section.sections'))

    return render_template('section_create.html')

# 板块详情
@section_bp.route('/detail/<int:section_id>')
def section_detail(section_id):
    section = Section.query.get_or_404(section_id)
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(section_id=section_id, deleted=False).paginate(page=page, per_page=10)
    return render_template('section_detail.html', section=section, posts=posts, pagination=posts)

# 板块分析
@section_bp.route('/analytics')
def section_analytics():
    # 获取版块活跃度排名
    section_post_counts = db.session.query(
        Section,
        func.count(Post.id).label('post_count')
    ).outerjoin(Post, Section.id == Post.section_id).filter(Post.deleted == False).group_by(Section.id).order_by(func.count(Post.id).desc()).all()

    # 获取近7天发帖趋势
    daily_post_counts = []
    for i in range(6, -1, -1):
        date = datetime.now() - timedelta(days=i)
        count = Post.query.filter(
            func.date(Post.created_at) == date.date(),
            Post.deleted == False
        ).count()
        daily_post_counts.append({
            'date': date.strftime('%Y-%m-%d'),
            'count': count
        })

    # 获取版块活跃用户
    section_active_users = {}
    for section in section_post_counts:
        users = db.session.query(
            User,
            func.count(Post.id).label('post_count')
        ).outerjoin(Post, User.id == Post.user_id).filter(
            Post.section_id == section.id,
            Post.deleted == False
        ).group_by(User.id).order_by(func.count(Post.id).desc()).limit(5).all()
        section_active_users[section.id] = users

    return render_template(
        'section_analytics.html',
        section_post_counts=section_post_counts,
        daily_post_counts=daily_post_counts,
        section_active_users=section_active_users
    )

# 编辑板块
@section_bp.route('/edit/<int:section_id>', methods=['GET', 'POST'])
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        icon = request.form.get('icon')

        if not name:
            flash('板块名称不能为空', 'error')
            return redirect(url_for('section.edit_section', section_id=section_id))

        # 检查板块名称是否已存在（排除当前板块）
        existing_section = Section.query.filter(
            Section.name == name,
            Section.id != section_id
        ).first()
        if existing_section:
            flash('该板块名称已存在', 'error')
            return redirect(url_for('section.edit_section', section_id=section_id))

        # 更新板块信息
        section.name = name
        section.description = description
        section.icon = icon

        db.session.commit()

        flash('板块更新成功', 'success')
        return redirect(url_for('section.sections'))

    return render_template('section_edit.html', section=section)

# 删除板块
@section_bp.route('/delete/<int:section_id>', methods=['POST'])
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)

    # 删除板块关联的帖子和评论
    posts = Post.query.filter_by(section_id=section_id).all()
    for post in posts:
        comments = Comment.query.filter_by(post_id=post.id).all()
        for comment in comments:
            db.session.delete(comment)
        db.session.delete(post)

    db.session.delete(section)
    db.session.commit()

    flash('板块删除成功', 'success')
    return redirect(url_for('section.sections'))