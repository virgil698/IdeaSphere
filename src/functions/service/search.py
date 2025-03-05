from flask import url_for, redirect, jsonify
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.functions.database.models import SearchModel, Post, Comment


def cosine_simulator(s1, s2):
    vectorizer = TfidfVectorizer().fit_transform([s1, s2])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]


def find_matches(data_field, field_name, keywords, threshold):
    matches = []
    for item in data_field:
        text = item.get('content') if field_name == '帖子内容' else item.get(
            'title') if field_name == '帖子标题' else item.get('author') if field_name == '作者' else item.get(
            'content')

        cosine_sim = cosine_simulator(keywords, text) if text else 0.0
        fuzzy_ratio = fuzz.token_sort_ratio(keywords, text) / 100.0 if text else 0.0

        combined_score = max(cosine_sim, fuzzy_ratio)

        if combined_score > threshold:
            preview = text[:100] + "..." if len(text) > 100 else text
            matches.append({
                'content': preview,
                'similarity': round(combined_score, 2),
                'source': field_name,
                'postId': item.get('id'),
                'commentId': item.get('commentId'),
                'matchType': 'fuzzy' if fuzzy_ratio > cosine_sim else 'cosine'
            })
    return sorted(matches, key=lambda x: x['similarity'], reverse=True)[:5]


def get_data():
    posts = Post.query.filter_by(deleted=False).all()
    comments = Comment.query.filter_by(deleted=False).all()

    posts_data = [{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username
    } for post in posts]

    comments_data = [{
        'id': comment.id,
        'content': comment.content,
        'author': comment.author.username,
        'postId': comment.post.id
    } for comment in comments]

    return {
        'posts': posts_data,
        'comments': comments_data
    }


def search_logic(keywords):
    if not keywords:
        return redirect(url_for('index'))

    keyword_results = SearchModel.query.filter(SearchModel.keyword.ilike(f'%{keywords}%')).all()
    if keyword_results:
        return jsonify({
            'success': True,
            'type': '关键词匹配',
            'results': [{} for k in keyword_results]
        })

    data = get_data()
    threshold = 0.2

    results = {
        '帖子标题': find_matches(data['posts'], '帖子标题', keywords, threshold),
        '帖子内容': find_matches(data['posts'], '帖子内容', keywords, threshold),
        '作者': find_matches(data['posts'], '作者', keywords, threshold),
        '评论内容': find_matches(data['comments'], '评论内容', keywords, threshold),
        '评论作者': find_matches(data['comments'], '评论作者', keywords, threshold)
    }

    all_results = []
    for result_type, matches in results.items():
        for match in matches:
            all_results.append({
                'source': result_type,
                'content': match['content'],
                'similarity': match['similarity'],
                'postId': match.get('postId'),
                'commentId': match.get('commentId')
            })

    all_results = sorted(all_results, key=lambda x: x['similarity'], reverse=True)[:20]

    if all_results:
        return jsonify({
            'success': True,
            'type': '内容匹配',
            'results': all_results
        })

    return jsonify({'success': False, 'message': '未找到相关结果'})