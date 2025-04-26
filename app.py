import os

import pytz
from flask import Flask, request, session, redirect, url_for, g, jsonify, render_template
from flask_apscheduler import APScheduler
from flask_wtf.csrf import CSRFProtect

from src.db_ext import db
from src.functions.api.api import api_bp  # 导入 API 蓝图
from src.functions.config.config import get_config, initialize_database
from src.functions.config.config_example import generate_config_example  # 导入生成示例配置文件的函数
from src.functions.database.models import User, Post, Comment  # 确保导入 Section 模型
from src.functions.icenter.db_operation import execute_sql_logic
from src.functions.icenter.icenter_index_page import icenter_index
from src.functions.icenter.icenter_login import icenter_login_logic
from src.functions.icenter.index_logic_for_icenter import return_icenter_index_templates, \
    return_icenter_execute_sql_templates, return_icenter_editor
from src.functions.index import index_logic, newest_logic, global_logic  # 导入新的逻辑函数
from src.functions.parser.markdown_parser import remove_markdown
from src.functions.perm.permission_groups import permission_group_logic
from src.functions.section.section import section_bp  # 导入板块蓝图
from src.functions.service import monitor
from src.functions.service.editor import editor_tool
from src.functions.service.intstall import install_logic
from src.functions.service.moderation import moderation_panel_logic, manage_reports_logic, manage_users_logic, \
    manage_posts_logic, \
    delete_post_logic
from src.functions.service.post_logic import create_post_logic, view_post_logic
from src.functions.service.search import search_logic
from src.functions.service.user_logic import register_logic, login_logic, logout_logic
from src.functions.service.user_operations import reply_logic, report_post_logic, like_post_logic, report_comment_logic, \
    like_comment_logic, upgrade_user_logic, downgrade_user_logic, handle_report_logic, edit_post_logic, \
    follow_user_logic, unfollow_user_logic, get_following_logic, get_followers_logic
from src.functions.service.user_routes import user_bp, scheduled_calculate_contributions  # 导入用户页面蓝图
from src.functions.utils.logger import Logger

"""
初始化部分   
"""
app = Flask(__name__, static_folder="static", static_url_path='/static', template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_should_be_complex")

# 生成示例配置文件
generate_config_example()

# 从配置文件中读取配置
config = get_config()

# 设置时区
timezone_str = config.get('timezone', 'UTC')
try:
    app.config['TIMEZONE'] = pytz.timezone(timezone_str)
except pytz.UnknownTimeZoneError:
    # 如果时区设置错误，使用默认的 UTC 时区
    app.config['TIMEZONE'] = pytz.utc
    print(f"Unknown timezone: {timezone_str}. Using UTC as default.")

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['uri']  # 动态设置数据库 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config['database']['track_modifications']

# CSRF配置
app.config['WTF_CSRF_ENABLED'] = config['csrf']['enabled']
app.config['WTF_CSRF_SSL_STRICT'] = config['csrf']['ssl_strict']

db.init_app(app)
csrf = CSRFProtect(app)

# 注册API蓝图
app.register_blueprint(api_bp, url_prefix='/api')

# 注册板块蓝图
app.register_blueprint(section_bp)  # 注册板块蓝图

# 注册用户页面蓝图
app.register_blueprint(user_bp)

app.jinja_env.globals.update(remove_markdown=remove_markdown)

# 初始化调度器
scheduler = APScheduler()

# 使用 Flask 应用上下文初始化调度器
with app.app_context():
    scheduler.init_app(app)
    scheduler.start()

# 配置定时任务
@scheduler.task('cron', id='calculate_contributions_task', minute='*/10')
def scheduled_task_every_10_minutes():
    # 确保在应用上下文中执行定时任务
    with app.app_context():
        scheduled_calculate_contributions()

@scheduler.task('cron', id='calculate_contributions_task_at_1am', hour=1, minute=0)
def scheduled_task_at_1am():
    # 确保在应用上下文中执行定时任务
    with app.app_context():
        scheduled_calculate_contributions()

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
    return index_logic()  # 默认重定向到时间线排序页面

@app.route('/newest')
def newest():
    return newest_logic()

@app.route('/global')
def global_sort():
    return global_logic()

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

@app.route('/moderation')
def moderation_panel():
    return moderation_panel_logic()

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

@app.route('/follow/<int:follower_id>/<int:following_id>', methods=['POST'])
def follow_user(follower_id, following_id):
    return follow_user_logic(follower_id, following_id)

@app.route('/unfollow/<int:follower_id>/<int:following_id>', methods=['POST'])
def unfollow_user(follower_id, following_id):
    return unfollow_user_logic(follower_id, following_id)

@app.route('/get_following/<int:user_id>')
def get_following(user_id):
    return get_following_logic(user_id)

@app.route('/get_followers/<int:user_id>')
def get_followers(user_id):
    return get_followers_logic(user_id)

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

@app.route('/front_end_log_interface/<string:message>/<string:mode>', methods=['POST', 'GET'])
def front_end_log_interface(message, mode):
    log_thread = Logger(
        threadID=1,
        name="FrontEnd",
        counter=1,
        msg=message,
        mode=mode,
        module_name="FrontEndInterface",
        log_path='./logs'
    )
    log_thread.start()
    return jsonify({'success': True})

@app.route('/save_file', methods=['POST', 'GET'])
def save_file():
    return editor_tool().save_file()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/reply/<string:front_end_reply_messsage>/<string:reply_to_users_id>', methods=['POST', 'GET'])
def reply(front_end_reply_messsage, reply_to_users_id):
    return reply_logic(front_end_reply_messsage, reply_to_users_id)

if __name__ == '__main__':
    # 初始化日志
    log_path = "./logs"  # 确保这个路径是正确的
    if not os.path.exists(log_path):
        os.makedirs(log_path, exist_ok=True)

    log_thread = Logger(
        threadID=1,
        name="LogThread",
        counter=1,
        msg="Initialize Log",
        mode="info",
        module_name="Server",
        log_path=log_path
    )
    log_thread.start()
    log_thread.package(config.get('log-size', 1000000000))
    from livereload import Server
    initialize_database(app)  # 调用数据库初始化函数
    server = Server(app.wsgi_app)
    # 监控templates文件夹下的所有文件改动
    server.watch('templates/**/*.*', ignore=None)
    server.serve(port=config.get('port', 5000), debug=config.get('debug', True))