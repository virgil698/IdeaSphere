from flask import request, session, flash, url_for, redirect
from werkzeug.security import check_password_hash

from src.functions.database.models import User


def icenter_login_logic():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(icenter_user=username).first()
        if user and check_password_hash(user.icenter_pwd, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('登录成功！', 'success')
            return redirect(url_for('real_icenter_index'))
        flash('用户名或密码错误', 'danger')
        return redirect(url_for('icenter'))