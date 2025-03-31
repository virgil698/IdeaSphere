import os
from flask import Flask, request, session, redirect, url_for, g
from flask_wtf.csrf import CSRFProtect
from src.db_ext import db
from src.functions.database.models import User, Post, Comment
from src.functions.icenter.db_operation import execute_sql_logic
from src.functions.index import index_logic
from src.functions.parser.markdown_parser import remove_markdown
from src.functions.perm.permission_groups import permission_group_logic
from src.functions.service.admin import admin_panel_logic, manage_reports_logic, manage_users_logic, manage_posts_logic, delete_post_logic
from src.functions.service.editor import editor_tool
from src.functions.service.intstall import install_logic
from src.functions.service.post_logic import create_post_logic, view_post_logic
from src.functions.service.search import search_logic
from src.functions.service.user_logic import register_logic, login_logic, logout_logic
from src.functions.service.user_operations import report_post_logic, like_post_logic, report_comment_logic, like_comment_logic, upgrade_user_logic, downgrade_user_logic, handle_report_logic, edit_post_logic
from src.functions.icenter.icenter_index_page import icenter_index
from src.functions.icenter.icenter_login import icenter_login_logic
from src.functions.icenter.index_logic_for_icenter import return_icenter_index_templates, \
    return_icenter_execute_sql_templates, return_icenter_editor
from src.functions.api.api import api_bp
from src.functions.config.config import get_config, initialize_database
from src.functions.service import monitor

"""
初始化部分   
"""
app = Flask(__name__, static_folder="templates/static", static_url_path='/static', template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_should_be_complex")

# 从配置文件中读取配置
config = get_config()

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['database']['track_modifications']

# CSRF配置
app.config['WTF_CSRF_ENABLED'] = config['csrf']['enabled']
app.config['WTF_CSRF_SSL_STRICT'] = config['csrf']['ssl_strict']

db.init_app(app)
csrf = CSRFProtect(app)

# 注册API蓝图
app.register_blueprint(api_bp, url_prefix='/api')

app.jinja_env.globals.update(remove_markdown=remove_markdown)

@app.before_request
def before_request():
    # 其他逻辑
    if 'user_id' not in session:
        if request.endpoint not in ['install', 'static'] and User.query.count() == 0:
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
    return execute_sql_logic()

@app.route('/sql_execute_page')
def sql_execute_page():
    return return_icenter_execute_sql_templates()

@app.route('/system_monitor/<string:mode>')
def system_monitor(mode):
    match (mode):
        case 'cpu':
            return monitor.SystemMonitor().get_cpu_usage_percent()
        case 'physics_info':
            return monitor.SystemMonitor().get_real_physics_usage()
        case 'memory':
            return monitor.SystemMonitor().get_memory_usage()
        case 'info':
            return monitor.SystemMonitor().get_basic_info_for_machine()

@app.route('/editor')
def editor():
    return return_icenter_editor()

@app.route('/directory_tree_api', methods=['GET'])
def directory_tree_api():
    return editor_tool().directory_tree()

@app.route('/get_file_content', methods=['POST'])
def get_file_content():
    return editor_tool().get_file_content()

if __name__ == '__main__':
    from livereload import Server
    initialize_database(app)  # 调用数据库初始化函数
    server = Server(app.wsgi_app)
    # 监控templates文件夹下的所有文件改动
    server.watch('templates/**/*.*', ignore=None)
    server.serve(port=config.get('port', 5000), debug=config.get('debug', True))