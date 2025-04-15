from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.db_ext import db
from src.functions.database.models import Section, Post, Comment, User
from src.functions.utils.logger import Logger
from datetime import datetime, timedelta
from sqlalchemy import func
from flask import abort

# 创建蓝图
section_bp = Blueprint('section', __name__, url_prefix='/section')

# 获取所有板块
@section_bp.route('/')
def sections():
    sections = Section.query.all()
    for section in sections:
        # 动态更新帖子数量
        section.post_count = Post.query.filter_by(section_id=section.id, deleted=False).count()
        # 动态更新回复数量
        section.comment_count = Comment.query.join(Post).filter(
            Post.section_id == section.id,
            Post.deleted == False
        ).count()
    db.session.commit()
    return render_template('section/sections.html', sections=sections)

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
            post_count=0,  # 初始化为 0
            comment_count=0  # 初始化为 0
        )

        db.session.add(new_section)
        db.session.commit()

        flash('板块创建成功', 'success')
        return redirect(url_for('section.sections'))

    return render_template('section/section_create.html')


# 板块详情（重定向到时间线排序）
@section_bp.route('/detail/<int:section_id>')
def section_detail(section_id):
    return redirect(url_for('section.section_newest', section_id=section_id))

# 时间线排序（板块内）
@section_bp.route('/detail/<int:section_id>/newest')
def section_newest(section_id):
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 查询该板块下的帖子并按时间线排序
    posts = Post.query.filter_by(section_id=section_id, deleted=False).order_by(
        Post.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    section = Section.query.get_or_404(section_id)
    return render_template(
        'section/section_detail.html',
        section=section,
        posts=posts,
        pagination=posts,
        sort='timeline'
    )

# 全局排序（板块内）
@section_bp.route('/detail/<int:section_id>/global_sort')
def section_global_sort(section_id):
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 查询该板块下的帖子并按全局排序
    posts = Post.query.filter_by(section_id=section_id, deleted=False).order_by(
        Post.like_count.desc(),
        Post.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    section = Section.query.get_or_404(section_id)
    return render_template(
        'section/section_detail.html',
        section=section,
        posts=posts,
        pagination=posts,
        sort='global'
    )

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
    for section, post_count in section_post_counts:
        users = db.session.query(
            User,
            func.count(Post.id).label('post_count')
        ).outerjoin(Post, User.id == Post.author_id).filter(
            Post.section_id == section.id,  # 使用 section.id
            Post.deleted == False
        ).group_by(User.id).order_by(func.count(Post.id).desc()).limit(5).all()
        section_active_users[section.id] = users  # 使用 section.id

    return render_template(
        'section/section_analytics.html',
        section_post_counts=section_post_counts,
        daily_post_counts=daily_post_counts,
        section_active_users=section_active_users
    )

# 编辑板块
@section_bp.route('/edit/<int:section_id>', methods=['GET'])
def edit_section(section_id):
    section = Section.query.get_or_404(section_id)
    return render_template('section/section_edit.html', section=section)

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

    # 重置板块的帖子和回复数量
    section.post_count = 0
    section.comment_count = 0
    db.session.commit()

    db.session.delete(section)
    db.session.commit()

    flash('板块删除成功', 'success')
    return redirect(url_for('section.sections'))