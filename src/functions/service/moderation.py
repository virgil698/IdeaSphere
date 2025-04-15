from flask import abort, g, render_template, url_for, flash, redirect

from src.functions.database.models import Report, User, Post, db


def moderation_panel_logic():
    if g.role not in ['admin', 'moderator']:
        abort(403)

    reports = Report.query.all()
    users = User.query.all()
    return render_template('moderation/moderation_panel.html', reports=reports, users=users)


def manage_users_logic():
    if g.role not in ['admin', 'moderator']:
        abort(403)

    users = User.query.all()
    return render_template('moderation/manage_users.html', users=users)


def manage_reports_logic():
    if g.role not in ['admin', 'moderator']:
        abort(403)

    reports = Report.query.all()
    return render_template('moderation/manage_reports.html', reports=reports)


def manage_posts_logic():
    if g.role not in ['admin', 'moderator']:
        abort(403)
    posts = Post.query.all()
    return render_template('moderation/manage_posts.html', posts=posts)


def delete_post_logic(post_id):
    if g.role not in ['admin', 'moderator']:
        print(f"User {g.user_id} attempted to delete post {post_id} without permission.")
        abort(403)

    post = db.session.get(Post, post_id)
    if not post:
        print(f"Attempted to delete non-existent post {post_id}.")
        abort(404)

    try:
        db.session.delete(post)
        db.session.commit()
        print(f"Post {post_id} deleted successfully by user {g.user_id}.")
        flash('帖子删除成功！', 'success')
        return redirect(url_for('manage_posts'))
    except Exception as e:
        db.session.rollback()
        print(f"Failed to delete post {post_id}: {str(e)}")
        flash('删除帖子时发生错误，请重试。', 'danger')
        return redirect(url_for('manage_posts'))