import os
import yaml
from flask import Flask, request, session, redirect, url_for, g, make_response
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf
from src.db_ext import db
from src.functions.database.models import User, Post, Comment
from src.functions.index import index_logic
from src.functions.parser.markdown_parser import remove_markdown
from src.functions.perm.permission_groups import permission_group_logic
from src.functions.service.admin import admin_panel_logic, manage_reports_logic, manage_users_logic, manage_posts_logic, delete_post_logic
from src.functions.service.intstall import install_logic
from src.functions.service.post_logic import create_post_logic, view_post_logic
from src.functions.service.search import search_logic
from src.functions.service.user_logic import register_logic, login_logic, logout_logic
from src.functions.service.user_operations import report_post_logic, like_post_logic, report_comment_logic, like_comment_logic, upgrade_user_logic, downgrade_user_logic, handle_report_logic, edit_post_logic
from src.functions.icenter.icenter_index_page import icenter_index

"""
初始化部分   
"""
app = Flask(__name__, static_folder="templates/static", static_url_path='/static', template_folder='templates')
app.secret_key = os.getenv("SECRET_KEY", "your_secret_key_should_be_complex")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置 CSRF 保护
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SSL_STRICT'] = True  # 如果使用 HTTPS，开启严格模式

db.init_app(app)
csrf = CSRFProtect(app)

def get_config():
    config_path = 'config.yml'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            yaml.dump({'port': 5000}, f)
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def initialize_database():
    with app.app_context():
        db.create_all()


app.jinja_env.globals.update(remove_markdown=remove_markdown)


@app.before_request
def before_request():
    # 设置 CSRF 令牌到 Cookie 中
    if 'csrf_token' not in session:
        session['csrf_token'] = generate_csrf()

    # 确保每次请求都设置 CSRF 令牌到 Cookie 中
    response = make_response()
    response.set_cookie('csrftoken', session['csrf_token'])

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

@csrf.exempt
@app.route('/install', methods=['GET', 'POST'])
def install():
    return install_logic()

@csrf.exempt
@app.route('/')
def index():
    return index_logic()

@csrf.exempt
@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_logic()

@csrf.exempt
@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_logic()

@csrf.exempt
@app.route('/logout')
def logout():
    return logout_logic()

@csrf.exempt
@app.route('/post', methods=['GET', 'POST'])
def create_post():
    return create_post_logic()

@csrf.exempt
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def view_post(post_id):
    return view_post_logic(post_id)

@csrf.exempt
@app.route('/admin')
def admin_panel():
    return admin_panel_logic()

@csrf.exempt
@app.route('/manage_users')
def manage_users():
    return manage_users_logic()

@csrf.exempt
@app.route('/manage_reports')
def manage_reports():
    return manage_reports_logic()

@csrf.exempt
@app.route('/report_post/<int:post_id>', methods=['POST'])
def report_post(post_id):
    return report_post_logic(post_id)

@csrf.exempt
@app.route('/report_comment/<int:comment_id>', methods=['POST'])
def report_comment(comment_id):
    return report_comment_logic(comment_id)

@csrf.exempt
@app.route('/like_post/<int:post_id>', methods=['POST'])
def like_post(post_id):
    return like_post_logic(post_id)

@csrf.exempt
@app.route('/like_comment/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
    return like_comment_logic(comment_id)

@csrf.exempt
@app.route('/upgrade_user/<int:user_id>')
def upgrade_user(user_id):
    return upgrade_user_logic(user_id)

@csrf.exempt
@app.route('/downgrade_user/<int:user_id>')
def downgrade_user(user_id):
    return downgrade_user_logic(user_id)

@csrf.exempt
@app.route('/handle_report/<int:report_id>', methods=['POST'])
def handle_report(report_id):
    return handle_report_logic(report_id)

@csrf.exempt
@app.route('/search/<keywords>', methods=['GET'])
def search(keywords):
    return search_logic(keywords)

@csrf.exempt
@app.route('/manage_posts')
def manage_posts():
    return manage_posts_logic()

@csrf.exempt
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    return edit_post_logic(post_id)

@csrf.exempt
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    return delete_post_logic(post_id)

@csrf.exempt
@app.route('/perm_groups/<int:user_id>/<string:user_perm>/<string:operation>', methods=['GET', 'POST'])
def perm_groups(user_id, user_perm, operation):
    return permission_group_logic(user_id, user_perm, operation)

@csrf.exempt
@app.route('/icenter', methods=['GET', 'POST'])
def icenter():
    return icenter_index()

if __name__ == '__main__':
    config = get_config()
    initialize_database()
    app.run(port=config.get('port', 5000), debug=True)