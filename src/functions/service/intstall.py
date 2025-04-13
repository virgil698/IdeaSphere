import sys
import subprocess
import pkg_resources
from flask import render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash
from src.functions.database.models import User, db, InstallationStatus
import redis

def check_python_version():
    current_version = sys.version_info
    required_version = (3, 11)
    return current_version >= required_version, current_version, required_version

def check_dependencies():
    dependencies = []
    with open('requirements.txt', 'r') as f:
        requirements = f.read().splitlines()
    for requirement in requirements:
        if 'pytest' in requirement:
            continue
        try:
            pkg = pkg_resources.require(requirement)[0]
            dependencies.append({
                'name': pkg.project_name,
                'installed_version': pkg.version,
                'required_version': requirement,
                'status': 'success'
            })
        except pkg_resources.DistributionNotFound:
            dependencies.append({
                'name': requirement.split('==')[0] if '==' in requirement else requirement,
                'installed_version': '未安装',
                'required_version': requirement,
                'status': 'error'
            })
        except pkg_resources.VersionConflict:
            dependencies.append({
                'name': requirement.split('==')[0] if '==' in requirement else requirement,
                'installed_version': pkg_resources.get_distribution(requirement.split('==')[0]).version,
                'required_version': requirement,
                'status': 'error'
            })
    return dependencies

def check_redis():
    from src.functions.config.config import get_config
    config = get_config()
    redis_config = config.get('redis', {})
    try:
        redis_client = redis.StrictRedis(
            host=redis_config.get('host', 'localhost'),
            port=redis_config.get('port', 6379),
            db=redis_config.get('db', 0),
            password=redis_config.get('password', ''),
            decode_responses=True
        )
        redis_client.ping()  # 测试连接
        return True, "Redis 连接成功"
    except redis.exceptions.ConnectionError as e:
        return False, f"Redis 连接失败: {str(e)}"
    except Exception as e:
        return False, f"Redis 检查失败: {str(e)}"

def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def install_logic():
    python_version_ok, current_python_version, required_python_version = check_python_version()
    dependencies = check_dependencies()
    dependencies_installed = all(dependency['status'] == 'success' for dependency in dependencies)
    redis_ok, redis_message = check_redis()

    if request.method == 'POST':
        if request.form['step'] == '1':
            if not dependencies_installed:
                install_dependencies()
                flash('依赖安装成功！', 'success')
                return redirect(url_for('install'))
            return redirect(url_for('install'))

        elif request.form['step'] == '2':
            return redirect(url_for('install'))

        elif request.form['step'] == '3':
            username = request.form['username']
            password = request.form['password']
            password_confirm = request.form['password_confirm']

            if password != password_confirm:
                flash('密码和确认密码不一致！', 'danger')
                return redirect(url_for('install'))

            if not username or not password:
                flash('请填写所有必填项！', 'danger')
                return redirect(url_for('install'))

            # 检查用户是否已经存在
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('该用户名已被占用，请选择其他用户名！', 'danger')
                return redirect(url_for('install'))

            new_admin = User(
                username=username,
                password=generate_password_hash(password),
                role='admin',
                user_uid=1
            )
            db.session.add(new_admin)

            install_status = InstallationStatus.query.first()
            if not install_status:
                install_status = InstallationStatus(is_installed=True)
                db.session.add(install_status)
            else:
                install_status.is_installed = True

            db.session.commit()
            flash('论坛安装成功！请登录', 'success')

            return jsonify({
                'success': True,
                'message': '安装成功！',
                'redirect': url_for('login')
            })

    return render_template('install.html',
                           python_version_ok=python_version_ok,
                           current_python_version=current_python_version,
                           required_python_version=required_python_version,
                           dependencies=dependencies,
                           dependencies_installed=dependencies_installed,
                           redis_ok=redis_ok,
                           redis_message=redis_message)