"""
数据库模型
"""
from email.policy import default

from src.db_ext import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_uid = db.Column(db.Integer, unique=True, nullable=False)  # 新增UID字段
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), default='user')  # user, moderator, admin
    icenter_user = db.Column(db.String)
    icenter_pwd = db.Column(db.String)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    html_content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    comments = db.relationship(
        'Comment',
        backref=db.backref('post', lazy=True),
        cascade="all, delete-orphan",  # 新增级联删除
        passive_deletes=True  # 允许数据库级联删除
    )
    deleted = db.Column(db.Boolean, default=False)
    delete_reason = db.Column(db.Text)
    delete_time = db.Column(db.DateTime)
    like_count = db.Column(db.Integer, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    html_content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', ondelete='CASCADE'),  # 添加数据库级联
        nullable=False
    )
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
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


class SearchModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), unique=True, nullable=False)


class InstallationStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_installed = db.Column(db.Boolean, default=False)
