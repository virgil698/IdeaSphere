import pytest
from app import app, db, User, Post
import json

@pytest.fixture
def client():
    """测试客户端"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # 禁用 CSRF 检查（仅在测试中）
    with app.app_context():  # 激活应用上下文
        db.create_all()

        yield app.test_client()

        db.session.remove()
        db.drop_all()

def login(client, username, password):
    """模拟登录"""
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    """模拟登出"""
    return client.get('/logout', follow_redirects=True)

def test_user_registration(client):
    """测试用户注册"""
    # 注册用户
    response = client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    assert '注册成功！请登录' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串
    assert User.query.filter_by(username='testuser').first() is not None

    # 验证重复注册
    response = client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    assert '用户名已存在' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

def test_user_login(client):
    """测试用户登录"""
    # 注册用户
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)

    # 登录
    response = login(client, 'testuser', 'testpassword')
    assert '登录成功！' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

    # 测试未注册用户
    response = login(client, 'nonexistent', 'password')
    assert '用户名或密码错误' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

def test_create_post(client):
    """测试创建帖子"""
    # 注册用户并登录
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    login(client, 'testuser', 'testpassword')

    # 创建帖子
    response = client.post('/post', data=dict(
        title='测试帖子',
        content='这是一个测试帖子'
    ), follow_redirects=True)

    assert '帖子创建成功！' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串
    assert Post.query.filter_by(title='测试帖子').first() is not None

def test_view_post(client):
    """测试查看帖子"""
    # 注册用户并创建帖子
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    login(client, 'testuser', 'testpassword')

    client.post('/post', data=dict(
        title='测试帖子',
        content='这是一个测试帖子'
    ), follow_redirects=True)

    post = Post.query.first()

    # 查看帖子
    response = client.get(f'/post/{post.id}')
    assert '测试帖子' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串
    assert '这是一个测试帖子' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

def test_add_comment(client):
    """测试添加评论"""
    # 注册用户并创建帖子
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    login(client, 'testuser', 'testpassword')

    client.post('/post', data=dict(
        title='测试帖子',
        content='这是一个测试帖子'
    ), follow_redirects=True)

    post = Post.query.first()

    # 添加评论
    response = client.post(f'/post/{post.id}', data=dict(
        content='这是测试评论'
    ), follow_redirects=True)

    assert '评论添加成功！' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

def test_report_post(client):
    """测试举报帖子"""
    # 注册用户并创建帖子
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    login(client, 'testuser', 'testpassword')

    client.post('/post', data=dict(
        title='测试帖子',
        content='这是一个测试帖子'
    ), follow_redirects=True)

    post = Post.query.first()

    # 举报帖子
    response = client.post(f'/report_post/{post.id}', json=json.dumps(
        {'reason': '测试举报原因'}
    ), content_type='application/json')

    assert '举报成功！' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

def test_like_post(client):
    """测试点赞帖子"""
    # 注册用户并创建帖子
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    login(client, 'testuser', 'testpassword')

    client.post('/post', data=dict(
        title='测试帖子',
        content='这是一个测试帖子'
    ), follow_redirects=True)

    post = Post.query.first()

    # 点赞帖子
    response = client.post(f'/like_post/{post.id}', follow_redirects=True)
    assert '点赞成功' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

def test_search(client):
    """测试搜索功能"""
    # 创建帖子用于搜索
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    login(client, 'testuser', 'testpassword')

    client.post('/post', data=dict(
        title='搜索帖子',
        content='这是用于搜索的测试帖子'
    ), follow_redirects=True)

    # 搜索帖子
    response = client.get('/search/搜索帖子')
    assert '搜索帖子' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串

def test_delete_post(client):
    """测试删除帖子"""
    # 注册管理员用户
    client.post('/register', data=dict(
        username='admin',
        password='adminpassword'
    ), follow_redirects=True)
    login(client, 'admin', 'adminpassword')

    # 创建帖子
    client.post('/post', data=dict(
        title='待删除的帖子',
        content='这是待删除的测试帖子'
    ), follow_redirects=True)

    post = Post.query.first()

    # 删除帖子
    response = client.get(f'/delete_post/{post.id}', follow_redirects=True)
    assert '帖子删除成功！' in response.data.decode('utf-8')  # 修复：使用字符串而非字节字符串
    assert Post.query.get(post.id) is None