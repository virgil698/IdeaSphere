import re

import bleach
from bs4 import BeautifulSoup
from markdown import markdown


import re
import bleach
from bs4 import BeautifulSoup
from markdown import markdown


def convert_markdown_to_html(markdown_text):
    # 添加对banner的支持
    banner_patterns = {
        'tip': r'::: tip\s*(.*?)\s*:::',
        'info': r'::: info\s*(.*?)\s*:::',
        'danger': r'::: danger\s*(.*?)\s*:::',
        'warning': r'::: warning\s*(.*?)\s*:::'
    }

    for banner_type, pattern in banner_patterns.items():
        markdown_text = re.sub(
            pattern,
            lambda m: f'<div class="banner banner-{banner_type}"><i class="fa fa-exclamation-circle"></i> {m.group(1)}</div>',
            markdown_text,
            flags=re.DOTALL
        )

    html = markdown(markdown_text, extensions=['tables'])
    allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'hr', 'br', 'div',
                    'span', 'ul', 'ol', 'li', 'strong', 'em', 'code', 'blockquote',
                    'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'i']
    allowed_attributes = {
        'a': ['href', 'title', 'target'],
        'img': ['src', 'alt', 'width', 'height'],
        'div': ['class', 'style'],
        'span': ['class', 'style'],
        'table': ['class', 'style'],
        'td': ['class', 'style'],
        'th': ['class', 'style'],
        'tr': ['class', 'style'],
        'pre': ['class', 'style'],
        'code': ['class', 'style'],
        'blockquote': ['class', 'style'],
        'i': ['class']
    }

    sanitized_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        strip=True
    )
    soup = BeautifulSoup(sanitized_html, 'html.parser')

    # 为表格添加类
    for table in soup.find_all('table'):
        table['class'] = 'styled-table'

    # 添加CSS样式
    style_tag = soup.new_tag('style')
    style_tag.string = '''
    .styled-table {
        border-collapse: collapse;
        width: 100%;
    }
    .styled-table th, .styled-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .styled-table tr:hover {
        background-color: #f5f5f5;
    }
    .banner {
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid transparent;
        border-radius: 4px;
        display: flex;
        align-items: center;
    }
    .banner i {
        margin-right: 10px;
    }
    .banner-tip {
        border-color: #d4edda;
        background-color: #d4edda;
        color: #155724;
    }
    .banner-info {
        border-color: #d1ecf1;
        background-color: #d1ecf1;
        color: #0c5460;
    }
    .banner-danger {
        border-color: #f8d7da;
        background-color: #f8d7da;
        color: #721c24;
    }
    .banner-warning {
        border-color: #fff3cd;
        background-color: #fff3cd;
        color: #856404;
    }
    '''
    # 确保 <head> 标签存在
    if not soup.head:
        head_tag = soup.new_tag('head')
        soup.insert(0, head_tag)
    soup.head.append(style_tag)

    cleaned_html = str(soup)
    return cleaned_html


def remove_markdown(text):
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'`', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'\n-{3,}', '', text)
    text = re.sub(r'\n={3,}', '', text)
    text = re.sub(r'\n\* \n', '', text)
    text = re.sub(r'\n\d\.', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    return text