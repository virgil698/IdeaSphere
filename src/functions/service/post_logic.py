from datetime import datetime

from flask import flash, g, redirect, url_for, request, render_template, abort, jsonify
from src.functions.database.models import Post, db, Comment, Section, UserActivity
from src.functions.parser.markdown_parser import convert_markdown_to_html


def create_post_logic():
    if not g.user:
        flash('请先登录再创建帖子', 'danger')
        return redirect(url_for('login'))

    sections = Section.query.all()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        section_id = request.form.get('section_id')

        if not section_id:
            flash('请选择板块后才能发布帖子', 'danger')
            return render_template('post.html', sections=sections)

        html_content = convert_markdown_to_html(content)
        new_post = Post(
            title=title,
            content=content,
            html_content=html_content,
            author_id=g.user.id,
            section_id=section_id
        )
        db.session.add(new_post)
        db.session.commit()

        # 更新用户活动统计
        today = datetime.utcnow().date()  # 使用datetime.datetime.utcnow()
        activity = UserActivity.query.filter_by(user_uid=g.user.user_uid, date=today).first()
        if activity:
            activity.posts_count += 1
        else:
            activity = UserActivity(
                user_uid=g.user.user_uid,
                date=today,
                posts_count=1
            )
            db.session.add(activity)
        db.session.commit()

        flash('帖子创建成功！', 'success')
        return redirect(url_for('index'))
    return render_template('post.html', sections=sections)


def view_post_logic(post_id):
    post = Post.query.get(post_id)
    if not post:
        abort(404)

    if post.deleted:
        flash('该帖子已被删除', 'danger')
        return redirect(url_for('index'))

    section = post.section
    post.look_count += 1
    db.session.commit()

    if request.method == 'POST':
        if not g.user:
            flash('请先登录再进行评论', 'danger')
            return redirect(url_for('login'))

        if request.headers.get('Accept') == 'application/json':
            data = request.get_json()
            content = data.get('content')
        else:
            content = request.form['content']

        if not content:
            flash('评论内容不能为空', 'danger')
            return redirect(url_for('view_post', post_id=post.id))

        html_content = convert_markdown_to_html(content)
        new_comment = Comment(
            content=content,
            html_content=html_content,
            author_id=g.user.id,
            post_id=post.id
        )
        db.session.add(new_comment)
        db.session.commit()

        # 更新用户活动统计
        today = datetime.utcnow().date()  # 使用datetime.datetime.utcnow()
        activity = UserActivity.query.filter_by(user_uid=g.user.user_uid, date=today).first()
        if activity:
            activity.comments_count += 1
        else:
            activity = UserActivity(
                user_uid=g.user.user_uid,
                date=today,
                comments_count=1
            )
            db.session.add(activity)
        db.session.commit()

        if request.headers.get('Accept') == 'application/json':
            return jsonify({'message': 'Comment created successfully', 'comment_id': new_comment.id}), 201
        else:
            flash('评论添加成功！', 'success')
            return redirect(url_for('view_post', post_id=post.id))

    comments = Comment.query.filter_by(post_id=post.id, deleted=False).all()
    return render_template('view_post.html', post=post, comments=comments, section=section)