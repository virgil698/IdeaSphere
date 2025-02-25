import os
import yaml
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, g, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import markdown
from datetime import datetime
from flask_wtf.csrf import CSRFProtect
import re

from bs4 import BeautifulSoup
from html_sanitizer import Sanitizer

app = Flask(__name__, template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_should_be_complex")
csrf = CSRFProtect(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# 数据库模型定义
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), default='user')  # user, moderator, admin


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    html_content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    deleted = db.Column(db.Boolean, default=False)
    delete_reason = db.Column(db.Text)
    delete_time = db.Column(db.DateTime)
    like_count = db.Column(db.Integer, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    html_content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))
    deleted = db.Column(db.Boolean, default=False)
    delete_reason = db.Column(db.Text)
    delete_time = db.Column(db.DateTime)
    like_count = db.Column(db.Integer, default=0)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('reports', lazy=True))
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref=db.backref('resolved_reports', lazy=True))
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, closed
    post = db.relationship('Post', foreign_keys=[post_id], backref=db.backref('reports', lazy=True))
    comment = db.relationship('Comment', foreign_keys=[comment_id], backref=db.backref('reports', lazy=True))


class Like(db.Model):
    __table_args__ = (
        db.CheckConstraint(
            '(post_id IS NOT NULL AND comment_id IS NULL) OR (post_id IS NULL AND comment_id IS NOT NULL)',
            name='check_like_target'
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)


# 配置文件读取
def get_config():
    config_path = 'config.yml'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            yaml.dump({'port': 5000}, f)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


# 初始化数据库
def initialize_database(app):
    with app.app_context():
        db.create_all()


# Markdown转换 + XSS过滤
def convert_markdown_to_html(markdown_text):
    # 使用 markdown 库的安全模式
    html = markdown.markdown(markdown_text, safe_mode='escape')

    # 定义允许的标签和属性
    allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'hr', 'br', 'div',
                    'span', 'ul', 'ol', 'li', 'strong', 'em', 'code', 'blockquote',
                    'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td']
    allowed_attributes = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'width', 'height'],
        '*': ['class', 'style'],
        'div': ['class', 'style'],
        'span': ['class', 'style'],
        'table': ['class', 'style'],
        'td': ['class', 'style'],
        'th': ['class', 'style'],
        'tr': ['class', 'style'],
        'pre': ['class', 'style'],
        'code': ['class', 'style'],
        'blockquote': ['class', 'style']
    }

    # 使用 html-sanitizer 进行清理
    sanitizer = Sanitizer(
        tags=allowed_tags,
        attributes=allowed_attributes
    )
    sanitized_html = sanitizer.sanitize(html)

    # 使用 BeautifulSoup 再次清理和一致化
    soup = BeautifulSoup(sanitized_html, 'html.parser')
    cleaned_html = str(soup)

    return cleaned_html


def remove_markdown(text):
    text = re.sub(r'\*\*', '', text)  # 去除粗体
    text = re.sub(r'\*', '', text)  # 去除斜体
    text = re.sub(r'`', '', text)  # 去除代码块
    text = re.sub(r'#', '', text)  # 去除标题
    text = re.sub(r'\n-{3,}', '', text)  # 去除水平线
    text = re.sub(r'\n={3,}', '', text)  # 去除水平线
    text = re.sub(r'\n\* \n', '', text)  # 去除列表
    text = re.sub(r'\n\d\.', '', text)  # 去除有序列表
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # 去除图片
    return text


app.jinja_env.globals.update(remove_markdown=remove_markdown)


# 前置请求
@app.before_request
def before_request():
    if 'user_id' not in session:
        if request.endpoint not in ['install', 'static'] and User.query.count() == 0:
            return redirect(url_for('install'))

    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            g.user = user
            g.role = user.role
        else:
            session.pop('user_id', None)
            g.user = None
            g.role = None
    else:
        g.user = None
        g.role = None

    user_agent = request.headers.get('User-Agent', 'Unknown')
    g.user_agent = user_agent


@app.context_processor
def inject_online_users():
    online_users = {'total': 0, 'users': 0, 'guests': 0, 'users_list': []}
    if g.user:
        online_users['total'] += 1
        online_users['users'] += 1
        online_users['users_list'].append(g.user.username)
    else:
        online_users['total'] += 1
        online_users['guests'] += 1
    return dict(online_users=online_users)


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


@app.route('/')
def index():
    posts = Post.query.filter_by(deleted=False).all()
    return render_template('index.html', posts=posts)


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


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('退出登录成功！', 'success')
    return redirect(url_for('index'))


@app.route('/post', methods=['GET', 'POST'])
def create_post():
    if not g.user:
        flash('请先登录再创建帖子', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        html_content = convert_markdown_to_html(content)
        new_post = Post(
            title=title,
            content=content,
            html_content=html_content,
            author_id=g.user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash('帖子创建成功！', 'success')
        return redirect(url_for('index'))
    return render_template('post.html')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    if post.deleted:
        flash('该帖子已被删除', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        if not g.user:
            flash('请先登录再进行评论', 'danger')
            return redirect(url_for('login'))

        content = request.form['content']
        html_content = convert_markdown_to_html(content)
        new_comment = Comment(
            content=content,
            html_content=html_content,
            author_id=g.user.id,
            post_id=post.id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('评论添加成功！', 'success')
        return redirect(url_for('view_post', post_id=post.id))

    # 使用 SQLAlchemy 的 ORM 查询过滤评论
    comments = db.session.query(Comment).filter(
        Comment.post_id == post.id,
        Comment.deleted == False
    ).all()

    return render_template('view_post.html', post=post, comments=comments)


@app.route('/admin')
def admin_panel():
    if g.role not in ['admin', 'moderator']:
        abort(403)

    reports = Report.query.all()
    users = User.query.all()
    return render_template('admin_panel.html', reports=reports, users=users)


@app.route('/report_post/<int:post_id>', methods=['POST'])
def report_post(post_id):
    if not g.user:
        return jsonify({'success': False, 'message': '请登录后再进行举报'}), 403

    reason = request.form.get('reason', '')
    if not reason:
        return jsonify({'success': False, 'message': '举报原因不能为空'}), 400

    existing_report = Report.query.filter_by(post_id=post_id, user_id=g.user.id).first()
    if existing_report:
        return jsonify({'success': False, 'message': '您已经举报过此帖子'}), 400

    new_report = Report(post_id=post_id, user_id=g.user.id, reason=reason)
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'success': True, 'message': '举报成功！'}), 200


@app.route('/report_comment/<int:comment_id>', methods=['POST'])
def report_comment(comment_id):
    if not g.user:
        return jsonify({'success': False, 'message': '请登录后再进行举报'}), 403

    reason = request.form.get('reason', '')
    if not reason:
        return jsonify({'success': False, 'message': '举报原因不能为空'}), 400

    existing_report = Report.query.filter_by(comment_id=comment_id, user_id=g.user.id).first()
    if existing_report:
        return jsonify({'success': False, 'message': '您已经举报过此评论'}), 400

    new_report = Report(comment_id=comment_id, user_id=g.user.id, reason=reason)
    db.session.add(new_report)
    db.session.commit()
    return jsonify({'success': True, 'message': '举报成功！'}), 200


@app.route('/upgrade_user/<int:user_id>')
def upgrade_user(user_id):
    if g.role != 'admin':
        abort(403)

    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    user.role = 'moderator'
    db.session.commit()
    flash('用户已提升为版主', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/downgrade_user/<int:user_id>')
def downgrade_user(user_id):
    if g.role != 'admin':
        abort(403)

    user = db.session.get(User, user_id)
    if not user:
        abort(404)

    user.role = 'user'
    db.session.commit()
    flash('版主已降级为普通用户', 'success')
    return redirect(url_for('admin_panel'))


@app.route('/handle_report/<int:report_id>', methods=['POST'])
def handle_report(report_id):
    if g.role not in ['admin', 'moderator']:
        abort(403)

    report = db.session.get(Report, report_id)
    if not report:
        abort(404)

    status = request.json.get('status')
    if status not in ['valid', 'invalid']:
        return jsonify({'success': False, 'message': '无效的状态值'}), 400

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


@app.route('/like_post/<int:post_id>', methods=['POST'])
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

    post = Post.query.get(post_id)
    return jsonify({'success': True, 'like_count': post.like_count})


@app.route('/like_comment/<int:comment_id>', methods=['POST'])
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

    comment = Comment.query.get(comment_id)
    return jsonify({'success': True, 'like_count': comment.like_count})


if __name__ == '__main__':
    config = get_config()
    initialize_database(app)
    app.run(port=config.get('port', 5000), debug=True)