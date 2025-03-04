from flask import flash, g, redirect, url_for, request, render_template, abort

from src.functions.database.models import Post, db, Comment
from src.functions.parser.markdown_parser import convert_markdown_to_html


def create_post_logic():
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

def view_post_logic(post_id):
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

    comments = db.session.query(Comment).filter(
        Comment.post_id == post.id,
        Comment.deleted == False
    ).all()

    return render_template('view_post.html', post=post, comments=comments)
