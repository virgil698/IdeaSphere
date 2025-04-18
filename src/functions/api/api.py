"""
API
@Dev virgil698
"""
from datetime import datetime
import math

from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf, validate_csrf
from src.db_ext import db
from src.functions.database.models import Post, Comment, Report, Like, Section, User  # 确保导入 User 模型
import psutil
from src.functions.parser.markdown_parser import convert_markdown_to_html

# 创建一个API蓝图
api_bp = Blueprint('api', __name__)

# 获取CSRF Token的API
@api_bp.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return jsonify({'csrf_token': csrf_token})

# 示例：获取所有帖子的API
@api_bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'html_content': post.html_content,
            'author': post.author.username,
            'like_count': post.like_count,
            'created_at': post.created_at.isoformat()
        }
        post_list.append(post_data)
    return jsonify(post_list)

# 示例：获取单个帖子的API
@api_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'message': 'Post not found'}), 404
    post_data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'html_content': post.html_content,
        'author': post.author.username,
        'like_count': post.like_count,
        'created_at': post.created_at.isoformat()
    }
    return jsonify(post_data)

# 示例：创建新帖子的API
@api_bp.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({'message': 'Invalid data'}), 400
    # 确保用户已登录
    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401
    new_post = Post(
        title=data['title'],
        content=data['content'],
        html_content=convert_markdown_to_html(data['content']),
        author_id=request.user.id
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully', 'post_id': new_post.id}), 201

# 示例：点赞帖子的API
@api_bp.route('/post/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    # 确保用户已登录
    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401
    existing_like = Like.query.filter_by(user_id=request.user.id, post_id=post_id).first()
    if existing_like:
        return jsonify({'message': 'You have already liked this post'}), 400
    new_like = Like(user_id=request.user.id, post_id=post_id)
    db.session.add(new_like)
    db.session.query(Post).filter_by(id=post_id).update({'like_count': Post.like_count + 1})
    db.session.commit()
    return jsonify({'message': 'Post liked successfully'}), 200

# 示例：举报帖子的API
@api_bp.route('/post/<int:post_id>/report', methods=['POST'])
def report_post(post_id):
    # 确保用户已登录
    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or 'reason' not in data:
        return jsonify({'message': 'Invalid data'}), 400
    existing_report = Report.query.filter_by(post_id=post_id, user_id=request.user.id).first()
    if existing_report:
        return jsonify({'message': 'You have already reported this post'}), 400
    new_report = Report(post_id=post_id, user_id=request.user.id, reason=data['reason'])
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'message': 'Post reported successfully'}), 200

# 示例：评论帖子的API
@api_bp.route('/post/<int:post_id>/comment', methods=['POST'])
def create_comment(post_id):
    # 确保用户已登录
    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'message': 'Invalid data'}), 400
    new_comment = Comment(
        content=data['content'],
        html_content=convert_markdown_to_html(data['content']),
        author_id=request.user.id,
        post_id=post_id
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment created successfully', 'comment_id': new_comment.id}), 201

# 创建新板块的API
@api_bp.route('/section/create', methods=['POST'])
def create_section():
    # 验证 CSRF Token
    csrf_token = request.headers.get('X-CSRFToken')
    if not csrf_token:
        return jsonify({'message': 'CSRF Token missing'}), 403

    try:
        validate_csrf(csrf_token)
    except:
        return jsonify({'message': 'Invalid CSRF Token'}), 403

    name = request.json.get('name')
    description = request.json.get('description')
    icon = request.json.get('icon')

    if not name:
        return jsonify({'message': '板块名称不能为空'}), 400

    # 检查板块名称是否已存在
    existing_section = Section.query.filter_by(name=name).first()
    if existing_section:
        return jsonify({'message': '该板块名称已存在'}), 400

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

    return jsonify({'message': '板块创建成功', 'section_id': new_section.id}), 201

# 编辑板块的API
@api_bp.route('/section/edit/<int:section_id>', methods=['POST'])
def edit_section(section_id):
    # 验证 CSRF Token
    csrf_token = request.headers.get('X-CSRFToken')
    if not csrf_token:
        return jsonify({'message': 'CSRF Token missing'}), 403

    try:
        validate_csrf(csrf_token)
    except:
        return jsonify({'message': 'Invalid CSRF Token'}), 403

    name = request.json.get('name')
    description = request.json.get('description')
    icon = request.json.get('icon')

    if not name:
        return jsonify({'message': '板块名称不能为空'}), 400

    # 检查板块是否存在
    section = Section.query.get_or_404(section_id)

    # 检查板块名称是否已存在（排除当前板块）
    existing_section = Section.query.filter(
        Section.name == name,
        Section.id != section_id
    ).first()
    if existing_section:
        return jsonify({'message': '该板块名称已存在'}), 400

    # 更新板块信息
    section.name = name
    section.description = description
    section.icon = icon

    db.session.commit()

    return jsonify({'message': '板块更新成功', 'section_id': section.id}), 200

# 关注用户的API
@api_bp.route('/user/<int:user_id>/follow', methods=['POST'])
def follow_user(user_id):
    # 验证 CSRF Token
    csrf_token = request.headers.get('X-CSRFToken')
    if not csrf_token:
        return jsonify({'message': 'CSRF Token missing'}), 403

    try:
        validate_csrf(csrf_token)
    except:
        return jsonify({'message': 'Invalid CSRF Token'}), 403

    # 确保用户已登录
    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401

    # 检查是否已经关注
    existing_follow = request.user.following.filter_by(following_id=user_id).first()
    if existing_follow:
        return jsonify({'message': 'You have already followed this user'}), 400

    # 添加关注关系
    request.user.following.append(User(id=user_id))
    db.session.commit()

    return jsonify({'message': 'User followed successfully'}), 200

# 取消关注用户的API
@api_bp.route('/user/<int:user_id>/unfollow', methods=['POST'])
def unfollow_user(user_id):
    # 验证 CSRF Token
    csrf_token = request.headers.get('X-CSRFToken')
    if not csrf_token:
        return jsonify({'message': 'CSRF Token missing'}), 403

    try:
        validate_csrf(csrf_token)
    except:
        return jsonify({'message': 'Invalid CSRF Token'}), 403

    # 确保用户已登录
    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401

    # 检查是否已经关注
    existing_follow = request.user.following.filter_by(following_id=user_id).first()
    if not existing_follow:
        return jsonify({'message': 'You have not followed this user'}), 400

    # 移除关注关系
    request.user.following.remove(existing_follow)
    db.session.commit()

    return jsonify({'message': 'User unfollowed successfully'}), 200

# 在API请求中验证CSRF Token
@api_bp.before_request
def csrf_protect():
    if request.method == "POST":
        csrf_token = request.headers.get('X-CSRFToken')
        if not csrf_token:
            return jsonify({'message': 'CSRF Token missing'}), 403
        # 验证CSRF Token
        if not validate_csrf_token(csrf_token):
            return jsonify({'message': 'Invalid CSRF Token'}), 403

# 验证CSRF Token的函数
def validate_csrf_token(token):
    try:
        validate_csrf(token)
        return True
    except:
        return False