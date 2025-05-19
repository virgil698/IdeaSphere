"""
API
@Dev virgil698
"""

from flask import Blueprint, jsonify, request
from flask_wtf.csrf import generate_csrf, validate_csrf

from src.db_ext import db
from src.functions.database.models import Post, Comment, Report, Like, Section, UserFollowerCount, \
    UserFollowRelation, UserFollowingCount, ReplyComment
from src.functions.parser.markdown_parser import convert_markdown_to_html
from src.functions.service.user_operations import reply_logic

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

# 举报帖子的API
@api_bp.route('/report_post/<int:post_id>', methods=['POST'])
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

# 举报评论的API
@api_bp.route('/report_comment/<int:comment_id>', methods=['POST'])
def report_comment(comment_id):
    # 确保用户已登录
    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or 'reason' not in data:
        return jsonify({'message': 'Invalid data'}), 400
    existing_report = Report.query.filter_by(comment_id=comment_id, user_id=request.user.id).first()
    if existing_report:
        return jsonify({'message': 'You have already reported this comment'}), 400
    new_report = Report(comment_id=comment_id, user_id=request.user.id, reason=data['reason'])
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'message': 'Comment reported successfully'}), 200

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
@api_bp.route('/follow-user', methods=['POST'])
def follow_user():
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

    data = request.get_json()
    target_user_uid = data.get('target_user_uid')

    if not target_user_uid:
        return jsonify({'message': 'Missing target_user_uid'}), 400

    # 检查是否已经关注
    existing_follow = UserFollowRelation.query.filter_by(
        follower_user_uid=request.user.user_uid,
        following_user_uid=target_user_uid
    ).first()

    if existing_follow:
        return jsonify({'message': 'You have already followed this user'}), 400

    # 添加关注关系
    new_follow = UserFollowRelation(
        follower_user_uid=request.user.user_uid,
        following_user_uid=target_user_uid
    )
    db.session.add(new_follow)

    # 更新粉丝数量（被关注者）
    follower_count_entry = UserFollowerCount.query.filter_by(
        user_user_uid=target_user_uid
    ).first()

    if follower_count_entry:
        follower_count_entry.follower_count += 1
    else:
        new_follower_count = UserFollowerCount(
            user_user_uid=target_user_uid,
            follower_count=1
        )
        db.session.add(new_follower_count)

    # 更新关注数量（当前用户）
    following_count_entry = UserFollowingCount.query.filter_by(
        user_user_uid=request.user.user_uid
    ).first()

    if following_count_entry:
        following_count_entry.following_count += 1
    else:
        new_following_count = UserFollowingCount(
            user_user_uid=request.user.user_uid,
            following_count=1
        )
        db.session.add(new_following_count)

    db.session.commit()

    return jsonify({'success': True, 'message': 'User followed successfully'}), 200

# 取消关注用户的API
@api_bp.route('/unfollow-user', methods=['POST'])
def unfollow_user():
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

    data = request.get_json()
    target_user_uid = data.get('target_user_uid')

    if not target_user_uid:
        return jsonify({'message': 'Missing target_user_uid'}), 400

    # 查找关注记录
    existing_follow = UserFollowRelation.query.filter_by(
        follower_user_uid=request.user.user_uid,
        following_user_uid=target_user_uid
    ).first()

    if not existing_follow:
        return jsonify({'message': 'You have not followed this user'}), 400

    # 删除关注关系
    db.session.delete(existing_follow)

    # 更新粉丝数量（被关注者）
    follower_count_entry = UserFollowerCount.query.filter_by(
        user_user_uid=target_user_uid
    ).first()

    if follower_count_entry:
        follower_count_entry.follower_count -= 1
        if follower_count_entry.follower_count < 0:
            follower_count_entry.follower_count = 0

    # 更新关注数量（当前用户）
    following_count_entry = UserFollowingCount.query.filter_by(
        user_user_uid=request.user.user_uid
    ).first()

    if following_count_entry:
        following_count_entry.following_count -= 1
        if following_count_entry.following_count < 0:
            following_count_entry.following_count = 0

    db.session.commit()

    return jsonify({'success': True, 'message': 'User unfollowed successfully'}), 200

# 评论回复的 API
@api_bp.route('/comment/<int:comment_id>/reply', methods=['POST'])
def reply_to_comment(comment_id):
    csrf_token = request.headers.get('X-CSRFToken')
    if not csrf_token:
        return jsonify({'message': 'CSRF Token missing'}), 403

    try:
        validate_csrf(csrf_token)
    except:
        return jsonify({'message': 'Invalid CSRF Token'}), 403

    if not request.user:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'message': 'Invalid data'}), 400

    reply_content = data['content']
    result = reply_logic(comment_id, reply_content)
    return result

# 获取评论的回复数量
@api_bp.route('/comment/<int:comment_id>/reply_count', methods=['GET'])
def get_comment_reply_count(comment_id):
    reply_count = Comment.query.filter_by(target_comment_id=comment_id).count()
    return jsonify({'reply_count': reply_count})

# 获取评论回复列表的 API
@api_bp.route('/comment/<int:comment_id>/replies', methods=['GET'])
def get_comment_replies(comment_id):
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 每页显示10条回复

    # 获取评论回复列表
    replies = ReplyComment.query.filter_by(target_comment_id=comment_id).\
        order_by(ReplyComment.like_count.desc(), ReplyComment.reply_at.desc())

    # 使用关键字参数调用 paginate 方法
    paginated_replies = replies.paginate(page=page, per_page=per_page, error_out=False)

    # 准备返回数据
    reply_list = []
    for reply in paginated_replies.items:
        reply_list.append({
            'id': reply.id,
            'content': reply.reply_message,
            'author': reply.reply_user,
            'created_at': reply.reply_at.isoformat(),
            'like_count': reply.like_count
        })

    return jsonify({
        'reply_list': reply_list,
        'page': paginated_replies.page,
        'pages': paginated_replies.pages,
        'has_prev': paginated_replies.has_prev,
        'has_next': paginated_replies.has_next,
        'prev_num': paginated_replies.prev_num if paginated_replies.has_prev else None,
        'next_num': paginated_replies.next_num if paginated_replies.has_next else None
    })

@api_bp.route('/comment/<int:comment_id>/replies_summary', methods=['GET'])
def get_comment_replies_summary(comment_id):
    # 获取回复总数
    total_replies = ReplyComment.query.filter_by(target_comment_id=comment_id).count()

    # 获取点赞数最高的1条回复
    top_liked_reply = ReplyComment.query.filter_by(target_comment_id=comment_id).\
        order_by(ReplyComment.like_count.desc()).first()

    # 获取最新发布的1条回复
    latest_reply = ReplyComment.query.filter_by(target_comment_id=comment_id).\
        order_by(ReplyComment.reply_at.desc()).first()

    top_replies = []
    if top_liked_reply:
        top_replies.append({
            'id': top_liked_reply.id,
            'content': top_liked_reply.reply_message,
            'author': top_liked_reply.reply_user,
            'created_at': top_liked_reply.reply_at.isoformat(),
            'like_count': top_liked_reply.like_count
        })

    if latest_reply and latest_reply.id != (top_liked_reply.id if top_liked_reply else None):
        top_replies.append({
            'id': latest_reply.id,
            'content': latest_reply.reply_message,
            'author': latest_reply.reply_user,
            'created_at': latest_reply.reply_at.isoformat(),
            'like_count': latest_reply.like_count
        })

    return jsonify({
        'total_replies': total_replies,
        'top_replies': top_replies
    })

# # 点赞回复的 API
# @api_bp.route('/reply/<int:reply_id>/like', methods=['POST'])
# def like_reply(reply_id):
#     # 验证 CSRF Token
#     csrf_token = request.headers.get('X-CSRFToken')
#     if not csrf_token:
#         return jsonify({'message': 'CSRF Token missing'}), 403
#
#     try:
#         validate_csrf(csrf_token)
#     except:
#         return jsonify({'message': 'Invalid CSRF Token'}), 403
#
#     # 确保用户已登录
#     if not request.user:
#         return jsonify({'message': 'Unauthorized'}), 401
#
#     # 检查是否已经点赞
#     existing_like = Like.query.filter_by(user_id=request.user.id, comment_id=reply_id).first()
#     if existing_like:
#         return jsonify({'message': 'You have already liked this reply', 'success': False}), 400
#
#     new_like = Like(user_id=request.user.id, comment_id=reply_id)
#     db.session.add(new_like)
#     db.session.commit()
#
#     # 获取更新后的点赞数
#     updated_like_count = Like.query.filter_by(comment_id=reply_id).count()
#
#     return jsonify({
#         'message': 'Reply liked successfully',
#         'success': True,
#         'like_count': updated_like_count
#     }), 200
#
# # 举报回复的 API
# @api_bp.route('/reply/<int:reply_id>/report', methods=['POST'])
# def report_reply(reply_id):
#     # 验证 CSRF Token
#     csrf_token = request.headers.get('X-CSRFToken')
#     if not csrf_token:
#         return jsonify({'message': 'CSRF Token missing'}), 403
#
#     try:
#         validate_csrf(csrf_token)
#     except:
#         return jsonify({'message': 'Invalid CSRF Token'}), 403
#
#     # 确保用户已登录
#     if not request.user:
#         return jsonify({'message': 'Unauthorized'}), 401
#
#     data = request.get_json()
#     if not data or 'reason' not in data:
#         return jsonify({'message': 'Invalid data', 'success': False}), 400
#
#     # 检查是否已经举报
#     existing_report = Report.query.filter_by(user_id=request.user.id, comment_id=reply_id).first()
#     if existing_report:
#         return jsonify({'message': 'You have already reported this reply', 'success': False}), 400
#
#     new_report = Report(comment_id=reply_id, user_id=request.user.id, reason=data['reason'])
#     db.session.add(new_report)
#     db.session.commit()
#
#     return jsonify({
#         'message': 'Reply reported successfully',
#         'success': True
#     }), 200

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