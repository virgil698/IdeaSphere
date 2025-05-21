from flask import Blueprint, request, render_template, jsonify
from src.functions.service.search_logic import search_logic  # 从新文件导入

# 创建蓝图
search_bp = Blueprint('search_bp', __name__)

# 定义搜索API路由
@search_bp.route('/api/search', methods=['GET'])
def api_search():
    keyword = request.args.get('keyword')  # 从查询字符串获取关键词
    if not keyword:
        return jsonify({'success': False, 'message': '未提供搜索关键词'})

    results = search_logic(keyword)
    return jsonify(results)

# 定义搜索页面路由
@search_bp.route('/search', methods=['GET'])
def search_page():
    keyword = request.args.get('keyword')  # 从查询字符串获取关键词
    if not keyword:
        return render_template('search.html', results=None, keyword=None)

    results = search_logic(keyword)
    return render_template('search.html', results=results.get('results'), keyword=keyword)