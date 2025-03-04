from flask import redirect, url_for, request, flash, render_template
from werkzeug.security import generate_password_hash
from src.functions.database.models import User, db

"""
安装程序
"""
def install_logic():
    if User.query.count() > 0:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # 确保第一个用户的UID是1
        new_admin = User(
            username=username,
            password=generate_password_hash(password),
            role='admin',
            user_uid=1  # 设置UID为1
        )
        db.session.add(new_admin)
        db.session.commit()
        flash('管理员注册成功！请登录', 'success')
        return redirect(url_for('login'))
    return render_template('install.html')