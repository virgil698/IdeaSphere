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

    # 定义每种banner对应的Font图标
    banner_icons = {
        'tip': 'fa-bell',
        'info': 'fa-circle-info',
        'danger': 'fa-exclamation-triangle',
        'warning': 'fa-circle-exclamation'
    }

    for banner_type, pattern in banner_patterns.items():
        icon_class = banner_icons.get(banner_type, 'fa-exclamation-circle')
        markdown_text = re.sub(
            pattern,
            lambda m: f'<div class="banner banner-{banner_type}"><i class="fa {icon_class}"></i> {m.group(1)}</div>',
            markdown_text,
            flags=re.DOTALL
        )

    # 预处理嵌套无序列表的缩进
    # 检测星号或者+号-号前有两个空格即判断为嵌套无序列表项
    markdown_text = re.sub(r'(\n\s{2})(\*|\+|-)\s', r'\1    \2 ', markdown_text)

    # 启用tables、breaks和fenced_code扩展
    html = markdown(
        markdown_text,
        extensions=['tables', 'nl2br', 'fenced_code']
    )

    allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'hr', 'br', 'div',
                    'span', 'ul', 'ol', 'li', 'strong', 'em', 'code', 'blockquote',
                    'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'i']
    allowed_attributes = {
        'a': ['href', 'title', 'target', 'class', 'data-fancybox'],
        'img': ['src', 'alt', 'width', 'height', 'class', 'data-fancybox'],
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

    # 禁止清洗代码块的样式
    allowed_attributes['pre'] = ['class', 'style']
    allowed_attributes['code'] = ['class', 'style']

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

    # 为代码块添加样式
    for pre in soup.find_all('pre'):
        pre['class'] = 'code-block'
        pre['style'] = 'background-color: #282c34; color: #abb2bf; font-family: monospace; border-radius: 5px; overflow-x: auto; margin: 15px 0;'

    # 为小段代码添加样式
    for code in soup.find_all('code'):
        # 检测代码块的长度，如果长度小于等于1行，则认为是小段代码
        if len(code.text.split('\n')) <= 1:
            code['class'] = 'code-inline'
            code['style'] = 'background-color: #f5f5f5; padding: 2px 4px; border-radius: 3px; font-family: monospace;'
        else:
            code['class'] = 'code-block'
            code['style'] = 'background-color: #282c34; color: #abb2bf; font-family: monospace; border-radius: 5px; overflow-x: auto; margin: 15px 0;'

    # 为图片添加 FancyBox 支持
    for img in soup.find_all('img'):
        if 'src' in img.attrs:
            # 添加 FancyBox 所需的类和属性
            img['class'] = img.get('class', []) + ['fancybox']
            img['data-fancybox'] = 'gallery'
            img['data-caption'] = img.get('alt', '')

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
    .code-inline {
        background-color: #f5f5f5;
        padding: 2px 4px;
        border-radius: 3px;
        font-family: monospace;
    }
    .code-block {
        background-color: #282c34;
        color: #abb2bf;
        font-family: monospace;
        border-radius: 5px;
        overflow-x: auto;
        margin: 15px 0;
        position: relative;
    }
    .code-block::before {
        content: attr(data-language);
        position: absolute;
        top: 5px;
        right: 5px;
        background-color: #3e4451;
        color: #abb2bf;
        padding: 2px 5px;
        border-radius: 3px;
        font-size: 0.8em;
    }
    .line-numbers {
        float: left;
        text-align: right;
        padding: 10px 10px 10px 0;
        margin-right: 10px;
        color: #8da0c4;
        border-right: 1px solid #494d5f;
        user-select: none;
    }
    .line-numbers span {
        display: block;
        counter-increment: linenumber;
    }
    .line-numbers span:before {
        content: counter(linenumber);
        color: #8da0bf;
    }
    '''
    if not soup.head:
        head_tag = soup.new_tag('head')
        soup.insert(0, head_tag)
    soup.head.append(style_tag)

    # 添加 FancyBox 的 CSS 和 JS
    fancybox_css = soup.new_tag('link', rel='stylesheet', href='https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.css')
    fancybox_js = soup.new_tag('script', src='https://cdn.jsdelivr.net/npm/@fancyapps/ui@4.0/dist/fancybox.umd.js')
    fancybox_js_initialization = soup.new_tag('script')
    fancybox_js_initialization.string = '''
    document.addEventListener("DOMContentLoaded", function() {
        Fancybox.bind('[data-fancybox="gallery"]', {
            // 配置选项
            loop: true,
            buttons: ["zoom", "slideShow", "fullScreen", "thumbs", "close"],
            image: {
                zoom: true
            }
        });
    });
    '''
    soup.head.append(fancybox_css)
    soup.head.append(fancybox_js)
    soup.head.append(fancybox_js_initialization)

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