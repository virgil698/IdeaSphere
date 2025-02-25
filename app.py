import os
import yaml
from flask import Flask, render_template, request, redirect, url_for, session, flash, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import markdown
from datetime import datetime, timedelta
import re
from flask_wtf.csrf import CSRFProtect

# 创建 Flask 应用
app = Flask(__name__, template_folder='templates')
app.secret_key = "your_secret_key"
csrf = CSRFProtect(app)

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), default='user')  # user, moderator, admin

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)  # 存储 Markdown 内容
    html_content = db.Column(db.Text, nullable=False)  # 存储转换后的 HTML 内容
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    deleted = db.Column(db.Boolean, default=False)  # 是否被删除
    delete_reason = db.Column(db.Text)  # 删除原因
    delete_time = db.Column(db.DateTime)  # 删除时间
    like_count = db.Column(db.Integer, default=0)  # 点赞数量

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # 存储 Markdown 内容
    html_content = db.Column(db.Text, nullable=False)  # 存储转换后的 HTML 内容
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    deleted = db.Column(db.Boolean, default=False)  # 是否被删除
    delete_reason = db.Column(db.Text)  # 删除原因
    delete_time = db.Column(db.DateTime)  # 删除时间
    like_count = db.Column(db.Integer, default=0)  # 点赞数量

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, closed
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # 解决该举报的管理员

# 获取配置文件
def get_config():
    config_path = 'config.yml'
    if not os.path.exists(config_path):
        # 初始化配置文件
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump({'port': 5000}, f)
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

# 初始化数据库
def initialize_database(app):
    with app.app_context():
        db.create_all()

# 将 Markdown 转换为 HTML
def convert_markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text)

# 过滤 Markdown 标识符的函数
def remove_markdown(text):
    # 使用正则表达式移除 Markdown 标识符
    text = re.sub(r'\*\*', '', text)  # 移除粗体
    text = re.sub(r'\*', '', text)    # 移除斜体
    text = re.sub(r'`', '', text)     # 移除代码块
    text = re.sub(r'#', '', text)     # 移除标题
    text = re.sub(r'\n-{3,}', '', text)  # 移除水平线
    text = re.sub(r'\n={3,}', '', text)  # 移除水平线
    text = re.sub(r'\n\* \n', '', text)  # 移除无序列表
    text = re.sub(r'\n\d\.', '', text)   # 移除有序列表
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 移除图片
    return text

# 在 app.py 的顶部添加以下代码
app.jinja_env.globals.update(remove_markdown=remove_markdown)

# 检查是否已有用户，如果没有则跳转到安装页面
@app.before_request
def before_request():
    if 'user_id' not in session:
        if request.endpoint != 'install' and User.query.count() == 0:
            return redirect(url_for('install'))

# 在请求开始时记录用户在线状态
@app.before_request
def record_online_status():
    if 'user_id' in session:
        g.user = db.session.get(User, session['user_id'])
    else:
        g.user = None

# 在线人数统计
@app.context_processor
def inject_online_users():
    online_users = {
        'total': 0,
        'users': 0,
        'guests': 0,
        'users_list': []
    }
    if g.user:
        online_users['total'] += 1
        online_users['users'] += 1
        online_users['users_list'].append(g.user.username)
    else:
        online_users['total'] += 1
        online_users['guests'] += 1
    return dict(online_users=online_users)

# 安装页面
@app.route('/install', methods=['GET', 'POST'])
def install():
    if User.query.count() > 0:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        new_admin = User(
            username=username,
            password=generate_password_hash(password),
            role='admin'
        )
        db.session.add(new_admin)
        db.session.commit()
        flash('管理员注册成功！请登录', 'success')
        return redirect(url_for('login'))
    return render_template('install.html')

# 主页面
@app.route('/')
def index():
    posts = Post.query.filter_by(deleted=False).all()
    return render_template('index.html', posts=posts)

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('用户名已存在', 'danger')
            return redirect(url_for('register'))
        new_user = User(
            username=username,
            password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash('注册成功！请登录', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('登录成功！', 'success')
            return redirect(url_for('index'))
        flash('用户名或密码错误', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

# 退出登录
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('退出登录成功！', 'success')
    return redirect(url_for('index'))

# 发表帖子
@app.route('/post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        html_content = convert_markdown_to_html(content)
        user_id = session['user_id']
        new_post = Post(title=title, content=content, html_content=html_content, author_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        flash('帖子创建成功！', 'success')
        return redirect(url_for('index'))
    return render_template('post.html')

# 查看帖子详情
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.deleted:
        flash('该帖子已被删除', 'danger')
        return redirect(url_for('index'))
    comments = post.comments  # 确保获取所有评论
    if request.method == 'POST':
        content = request.form['content']
        html_content = convert_markdown_to_html(content)
        user_id = session['user_id']
        new_comment = Comment(content=content, html_content=html_content, author_id=user_id, post_id=post_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('评论添加成功！', 'success')
        return redirect(url_for('view_post', post_id=post_id))
    return render_template('view_post.html', post=post, comments=comments)

# 管理员后台
@app.route('/admin')
def admin_panel():
    if 'role' not in session or session['role'] not in ['admin', 'moderator']:
        flash('无权限访问', 'danger')
        return redirect(url_for('index'))
    reports = Report.query.filter_by(status='pending').all()
    users = User.query.all()
    return render_template('admin_panel.html', reports=reports, users=users)

# 举报帖子
@app.route('/report_post/<int:post_id>', methods=['POST'])
def report_post(post_id):
    if 'user_id' not in session:
        flash('请登录后再进行举报', 'danger')
        return redirect(url_for('login'))
    reason = request.form['reason']
    user_id = session['user_id']
    existing_report = Report.query.filter_by(post_id=post_id, user_id=user_id).first()
    if existing_report:
        flash('您已经举报过此帖子', 'warning')
        return redirect(url_for('view_post', post_id=post_id))
    new_report = Report(post_id=post_id, user_id=user_id, reason=reason)
    db.session.add(new_report)
    db.session.commit()
    flash('举报成功！', 'success')
    return redirect(url_for('view_post', post_id=post_id))

# 举报评论
@app.route('/report_comment/<int:comment_id>', methods=['POST'])
def report_comment(comment_id):
    if 'user_id' not in session:
        flash('请登录后再进行举报', 'danger')
        return redirect(url_for('login'))
    # 通过 comment_id 查询 Comment 对象
    comment = Comment.query.get_or_404(comment_id)
    reason = request.form['reason']
    user_id = session['user_id']
    # 检查是否已经举报过该评论
    existing_report = Report.query.filter_by(comment_id=comment_id, user_id=user_id).first()
    if existing_report:
        flash('您已经举报过此评论', 'warning')
        return redirect(url_for('view_post', post_id=comment.post_id))
    # 创建新的举报记录
    new_report = Report(comment_id=comment_id, user_id=user_id, reason=reason)
    db.session.add(new_report)
    db.session.commit()
    flash('举报成功！', 'success')
    return redirect(url_for('view_post', post_id=comment.post_id))

# 提升用户为版主
@app.route('/upgrade_user/<int:user_id>')
def upgrade_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('无权限操作', 'danger')
        return redirect(url_for('admin_panel'))
    user = User.query.get_or_404(user_id)
    user.role = 'moderator'
    db.session.commit()
    flash('用户已提升为版主', 'success')
    return redirect(url_for('admin_panel'))

# 降级版主为普通用户
@app.route('/downgrade_user/<int:user_id>')
def downgrade_user(user_id):
    if 'role' not in session or session['role'] != 'admin':
        flash('无权限操作', 'danger')
        return redirect(url_for('admin_panel'))
    user = User.query.get_or_404(user_id)
    user.role = 'user'
    db.session.commit()
    flash('版主已降级为普通用户', 'success')
    return redirect(url_for('admin_panel'))

# 删除帖子
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if 'role' not in session or session['role'] not in ['admin', 'moderator', 'user']:
        flash('无权限操作', 'danger')
        return redirect(url_for('index'))
    if session['role'] == 'user' and post.author_id != session['user_id']:
        flash('无权限操作', 'danger')
        return redirect(url_for('index'))
    post.deleted = True
    post.delete_reason = request.form['delete_reason']
    post.delete_time = datetime.now() + timedelta(hours=24)
    db.session.commit()
    flash('帖子将在24小时后彻底删除', 'success')
    return redirect(url_for('admin_panel'))

# 恢复帖子
@app.route('/restore_post/<int:post_id>')
def restore_post(post_id):
    if 'role' not in session or session['role'] not in ['admin', 'moderator']:
        flash('无权限操作', 'danger')
        return redirect(url_for('index'))
    post = Post.query.get_or_404(post_id)
    post.deleted = False
    db.session.commit()
    flash('帖子已恢复', 'success')
    return redirect(url_for('admin_panel'))

# 删除评论
@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if 'role' not in session or session['role'] not in ['admin', 'moderator', 'user']:
        flash('无权限操作', 'danger')
        return redirect(url_for('view_post', post_id=comment.post_id))
    if session['role'] == 'user' and comment.author_id != session['user_id']:
        flash('无权限操作', 'danger')
        return redirect(url_for('view_post', post_id=comment.post_id))
    comment.deleted = True
    comment.delete_reason = request.form['delete_reason']
    comment.delete_time = datetime.now() + timedelta(hours=24)
    db.session.commit()
    flash('评论将在24小时后彻底删除', 'success')
    return redirect(url_for('view_post', post_id=comment.post_id))

# 恢复评论
@app.route('/restore_comment/<int:comment_id>')
def restore_comment(comment_id):
    if 'role' not in session or session['role'] not in ['admin', 'moderator']:
        flash('无权限操作', 'danger')
        return redirect(url_for('index'))
    comment = Comment.query.get_or_404(comment_id)
    comment.deleted = False
    db.session.commit()
    flash('评论已恢复', 'success')
    return redirect(url_for('admin_panel'))

# 点赞帖子
@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '未登录'})
    post = Post.query.get_or_404(post_id)
    post.like_count += 1
    db.session.commit()
    return jsonify({'success': True, 'like_count': post.like_count})

# 点赞评论
@app.route('/like_comment/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '未登录'})
    comment = Comment.query.get_or_404(comment_id)
    comment.like_count += 1
    db.session.commit()
    return jsonify({'success': True, 'like_count': comment.like_count})

# 处理举报
@app.route('/handle_report/<int:report_id>', methods=['POST'])
def handle_report(report_id):
    if 'role' not in session or session['role'] not in ['admin', 'moderator']:
        return jsonify({'success': False, 'message': '无权限操作'})
    report = Report.query.get_or_404(report_id)
    status = request.json.get('status')
    if status == 'valid':
        if report.post:
            report.post.deleted = True
            report.post.delete_reason = report.reason
            report.post.delete_time = datetime.now() + timedelta(hours=24)
            report.status = 'closed'
            db.session.commit()
            return jsonify({'success': True, 'message': '已违规，帖子已隐藏'})
        else:
            return jsonify({'success': False, 'message': '无法找到被举报的帖子'})
    elif status == 'invalid':
        report.status = 'closed'
        db.session.commit()
        return jsonify({'success': True, 'message': '未违规，举报已关闭'})
    else:
        return jsonify({'success': False, 'message': '处理失败'})

# 在线人数页面
@app.route('/online_users')
def online_users():
    return render_template('online_users.html')

# 启动应用
if __name__ == '__main__':
    config = get_config()
    initialize_database(app)
    app.run(port=config.get('port', 5000), debug=True)