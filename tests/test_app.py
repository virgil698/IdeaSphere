import pytest
from app import app, db, User, Post, Comment, Report, Like
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login(client):
    response = client.post('/login', data={
        'username': 'test_user',
        'password': 'test_password'
    })
    assert response.status_code == 302  # Redirect to index

def test_register(client):
    response = client.post('/register', data={
        'username': 'test_user',
        'password': 'test_password'
    })
    assert response.status_code == 302  # Redirect to login

def test_create_post(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'user'
    response = client.post('/post', data={
        'title': 'Test Post',
        'content': 'This is a test post.'
    })
    assert response.status_code == 302  # Redirect to index

def test_view_post(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'user'
    post = Post(title='Test Post', content='This is a test post.', author_id=1)
    with app.app_context():
        db.session.add(post)
        db.session.commit()
    response = client.get(f'/post/{post.id}')
    assert response.status_code == 200

def test_report_post(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'user'
    post = Post(title='Test Post', content='This is a test post.', author_id=1)
    with app.app_context():
        db.session.add(post)
        db.session.commit()
    response = client.post(f'/report_post/{post.id}', json={'reason': 'Test reason'})
    assert response.status_code == 200
    assert response.json['success'] is True

def test_like_post(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'user'
    post = Post(title='Test Post', content='This is a test post.', author_id=1)
    with app.app_context():
        db.session.add(post)
        db.session.commit()
    response = client.post(f'/like_post/{post.id}')
    assert response.status_code == 200
    assert response.json['success'] is True

def test_admin_panel(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'admin'
    response = client.get('/admin')
    assert response.status_code == 200

def test_manage_users(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'admin'
    response = client.get('/manage_users')
    assert response.status_code == 200

def test_manage_reports(client):
    with client.session_transaction() as session:
        session['user_id'] = 1
        session['role'] = 'admin'
    response = client.get('/manage_reports')
    assert response.status_code == 200