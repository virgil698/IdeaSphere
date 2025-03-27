import os
import yaml
from flask import Flask, request, session, redirect, url_for, g, make_response, jsonify, flash
from flask_wtf.csrf import CSRFProtect, generate_csrf
from src.db_ext import db
from src.functions.database.models import User, Post, Comment, Report, Like, InstallationStatus
from src.functions.icenter.db_operation import execute_sql_statement
from src.functions.index import index_logic
from src.functions.parser.markdown_parser import remove_markdown, convert_markdown_to_html
from src.functions.perm.permission_groups import permission_group_logic
from src.functions.service.admin import admin_panel_logic, manage_reports_logic, manage_users_logic, manage_posts_logic, \
    delete_post_logic
from src.functions.service.post_logic import create_post_logic, view_post_logic
from src.functions.service.search import search_logic
from src.functions.service.user_logic import register_logic, login_logic, logout_logic
from src.functions.service.user_operations import report_post_logic, like_post_logic, report_comment_logic, \
    like_comment_logic, upgrade_user_logic, downgrade_user_logic, handle_report_logic, edit_post_logic
from src.functions.icenter.icenter_index_page import icenter_index
from src.functions.icenter.icenter_login import icenter_login_logic
from src.functions.icenter.index_logic_for_icenter import return_icenter_index_templates, \
    return_icenter_execute_sql_templates
from src.functions.api.api import api_bp  # 导入API蓝图
from src.functions.service.intstall import install_logic

"""
初始化部分   
"""
app = Flask(__name__, static_folder="templates/static", static_url_path='/templates/static', template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_should_be_complex")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SSL_STRICT'] = True  # 如果使用 HTTPS，开启严格模式

db.init_app(app)
csrf = CSRFProtect(app)

# 注册API蓝图
app.register_blueprint(api_bp, url_prefix='/api')


def get_config():
    config_path = 'config.yml'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            yaml.dump({'port': 5000, 'debug': True}, f)  # 默认配置
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def initialize_database():
    with app.app_context():
        db.create_all()
        # 创建安装状态记录
        if not InstallationStatus.query.first():
            db.session.add(InstallationStatus(is_installed=False))
            db.session.commit()


app.jinja_env.globals.update(remove_markdown=remove_markdown)


@app.before_request
def before_request():
    # 检查是否已经安装
    install_status = InstallationStatus.query.first()
    if install_status and install_status.is_installed:
        # 如果已经安装，且访问的是 install 页面，则重定向到登录页面
        if request.endpoint == 'install':
            return redirect(url_for('login'))
    else:
        # 如果未安装，且访问的不是 install 页面，则重定向到 install 页面
        if request.endpoint != 'install':
            return redirect(url_for('install'))

    # 其他逻辑
    if 'user_id' not in session:
        if request.endpoint not in ['install', 'static', 'login']:
            return redirect(url_for('install'))

    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
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
def inject_forum_stats():
    forum_stats = {
        'topics': Post.query.filter_by(deleted=False).count(),
        'messages': Comment.query.filter_by(deleted=False).count(),
        'users': User.query.count(),
        'latest_user': User.query.order_by(User.id.desc()).first().username if User.query.count() > 0 else "暂无用户"
    }
    return {'forum_stats': forum_stats}


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
    return {'online_users': online_users}


"""
路由部分
"""


@app.route('/install', methods=['GET', 'POST'])
def install():
    return install_logic()


@app.route('/')
def index():
    return index_logic()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_logic()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_logic()


@app.route('/logout')
def logout():
    return logout_logic()


@app.route('/post', methods=['GET', 'POST'])
def create_post():
    return create_post_logic()


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    return view_post_logic(post_id)


@app.route('/admin')
def admin_panel():
    return admin_panel_logic()


@app.route('/manage_users')
def manage_users():
    return manage_users_logic()


@app.route('/manage_reports')
def manage_reports():
    return manage_reports_logic()


@app.route('/report_post/<int:post_id>', methods=['POST'])
def report_post(post_id):
    return report_post_logic(post_id)


@app.route('/report_comment/<int:comment_id>', methods=['POST'])
def report_comment(comment_id):
    return report_comment_logic(comment_id)


@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    return like_post_logic(post_id)


@app.route('/like_comment/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
    return like_comment_logic(comment_id)


@app.route('/upgrade_user/<int:user_id>')
def upgrade_user(user_id):
    return upgrade_user_logic(user_id)


@app.route('/downgrade_user/<int:user_id>')
def downgrade_user(user_id):
    return downgrade_user_logic(user_id)


@app.route('/handle_report/<int:report_id>', methods=['POST'])
def handle_report(report_id):
    return handle_report_logic(report_id)


@app.route('/search/<keywords>', methods=['GET'])
def search(keywords):
    return search_logic(keywords)


@app.route('/manage_posts')
def manage_posts():
    return manage_posts_logic()


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    return edit_post_logic(post_id)


@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    return delete_post_logic(post_id)


@app.route('/perm_groups/<int:user_id>/<string:user_perm>/<string:operation>', methods=['GET', 'POST'])
def perm_groups(user_id, user_perm, operation):
    return permission_group_logic(user_id, user_perm, operation)


@app.route('/icenter', methods=['GET', 'POST'])
def icenter():
    return icenter_index()


@app.route('/icenter_login', methods=['GET', 'POST'])
def icenter_login():
    return icenter_login_logic()


"""
真正的ICENTER——INDEX
"""


@app.route('/real_icenter_index')
def real_icenter_index():
    return return_icenter_index_templates()


@app.route('/execute_sql', methods=['POST'])  # 改为仅接受POST请求
def execute_sql():
    # 从JSON请求体中获取SQL
    sql_statement = request.json.get('sql')

    if not sql_statement:
        return jsonify({
            "success": False,
            "message": "未提供SQL语句"
        }), 400

    # 执行并获取结果
    result = execute_sql_statement(sql_statement)

    # 返回标准JSON响应
    status_code = 200 if result['success'] else 500
    return jsonify(result), status_code


@app.route('/sql_execute_page')
def sql_execute_page():
    return return_icenter_execute_sql_templates()


if __name__ == '__main__':
    from livereload import Server

    config = get_config()
    initialize_database()
    server = Server(app.wsgi_app)
    # 监控templates文件夹下的所有文件改动
    server.watch('templates/**/*.*', ignore=None)
    server.serve(port=config.get('port', 5000), debug=config.get('debug', True))