import re
import bleach
from bs4 import BeautifulSoup
from markdown import markdown
from bleach.css_sanitizer import CSSSanitizer


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
        'tip': 'fa-lightbulb',
        'info': 'fa-circle-info',
        'danger': 'fa-skull',
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
    markdown_text = re.sub(r'(\n\s{2})(\*|\+|-)\s', r'\1    \2 ', markdown_text)

    # 启用tables、breaks和fenced_code扩展
    html = markdown(
        markdown_text,
        extensions=['tables', 'nl2br', 'fenced_code']
    )

    # 创建一个 CSSSanitizer 实例，允许常用的 CSS 属性
    css_sanitizer = CSSSanitizer(
        allowed_css_properties=[
            'color', 'font-size', 'font-weight', 'font-style', 'text-align',
            'background-color', 'border', 'border-radius', 'padding', 'margin',
            'width', 'height', 'display', 'flex', 'justify-content', 'align-items',
            'text-decoration', 'line-height', 'list-style-type', 'overflow',
            'overflow-x', 'overflow-y', 'white-space', 'word-wrap', 'word-break'
        ]
    )

    allowed_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'hr', 'br', 'div',
                    'span', 'ul', 'ol', 'li', 'strong', 'em', 'code', 'blockquote',
                    'a', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'i', 'iframe', 'blockquote', 'script']
    allowed_attributes = {
        'a': ['href', 'title', 'target', 'class', 'data-fancybox'],
        'img': ['src', 'alt', 'width', 'height', 'class', 'data-fancybox'],
        'div': ['class', 'style'],
        'span': ['class', 'style'],
        'table': ['class', 'style'],
        'td': ['class', 'style'],
        'th': ['class', 'style'],
        'tr': ['class', 'style'],
        'pre': ['class', 'style', 'data-line', 'data-line-offset', 'data-start'],
        'code': ['class', 'style', 'data-prismjs-copy', 'data-prismjs-copy-error', 'data-prismjs-copy-success', 'data-prismjs-copy-timeout'],
        'script': ['src', 'async'],
        'i': ['class'],
        'iframe': ['src','scrolling', 'border', 'framespacing', 'width', 'height', 'frameborder', 'allowfullscreen', 'allow', 'referrerpolicy'],
        'blockquote': ['class', 'cite', 'style']
    }

    # 清理 HTML 内容
    sanitized_html = bleach.clean(
        html,
        tags=allowed_tags,
        attributes=allowed_attributes,
        css_sanitizer=css_sanitizer,
        strip=True
    )

    soup = BeautifulSoup(sanitized_html, 'html.parser')

    # 添加 PrismJS 的 CSS 和 JS
    prism_css = soup.new_tag('link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-okaidia.min.css')
    prism_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js')
    prism_toolbar_css = soup.new_tag('link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/toolbar/prism-toolbar.min.css')
    prism_toolbar_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/toolbar/prism-toolbar.min.js')
    prism_line_numbers_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.js')
    prism_line_highlight_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-highlight/prism-line-highlight.min.js')
    prism_copy_to_clipboard_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js')
    prism_show_language_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/show-language/prism-show-language.min.js')

    if not soup.head:
        head_tag = soup.new_tag('head')
        soup.insert(0, head_tag)
    soup.head.append(prism_css)
    soup.head.append(prism_js)
    soup.head.append(prism_toolbar_css)
    soup.head.append(prism_toolbar_js)
    soup.head.append(prism_line_numbers_js)
    soup.head.append(prism_line_highlight_js)
    soup.head.append(prism_copy_to_clipboard_js)
    soup.head.append(prism_show_language_js)

    # 处理代码块
    for code_block in soup.find_all('code'):
        parent_pre = code_block.find_parent('pre')
        if parent_pre:
            # 添加 PrismJS 需要的类
            parent_pre['class'] = parent_pre.get('class', []) + ['line-numbers']
            # 添加代码语言信息
            if 'class' in code_block.attrs:
                for cls in code_block['class']:
                    if cls.startswith('language-'):
                        code_block['class'] = [cls]
                        break
            else:
                code_block['class'] = ['language-text']

    # 添加 CSS 样式
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
        border-color: #e6f6e6;
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
    .tiktok-embed {
        margin: 20px 0;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        background-color: #f9f9f9;
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

    # 处理图片添加 FancyBox 支持
    for img in soup.find_all('img'):
        if 'src' in img.attrs:
            img['class'] = img.get('class', []) + ['fancybox']
            img['data-fancybox'] = 'gallery'
            img['data-caption'] = img.get('alt', '')

    # 处理 iframe 嵌入代码
    for iframe in soup.find_all('iframe'):
        if 'src' in iframe.attrs:
            src = iframe['src']
            # 处理 B 站视频嵌入
            if re.match(r'//player\.bilibili\.com/player\.html\?isOutside=true&.*', src):
                iframe['width'] = iframe.get('width', '640')
                iframe['height'] = iframe.get('height', '360')
                iframe['allowfullscreen'] = iframe.get('allowfullscreen', 'true')
            # 处理优酷视频嵌入
            elif re.match(r'https?://player\.youku\.com/embed/.*', src):
                iframe['width'] = iframe.get('width', '510')
                iframe['height'] = iframe.get('height', '498')
                iframe['frameborder'] = iframe.get('frameborder', '0')
                iframe['allowfullscreen'] = iframe.get('allowfullscreen', 'true')
            # 处理网易云音乐播放器嵌入
            elif re.match(r'//music\.163\.com/outchain/player\?type=2&.*', src):
                iframe['width'] = iframe.get('width', '330')
                iframe['height'] = iframe.get('height', '86')
                iframe['frameborder'] = iframe.get('frameborder', 'no')
                iframe['border'] = iframe.get('border', '0')
            # 处理网易云音乐歌单嵌入
            elif re.match(r'//music\.163\.com/outchain/player\?type=0&.*', src):
                if 'height=430' in src:
                    iframe['width'] = iframe.get('width', '330')
                    iframe['height'] = iframe.get('height', '450')
                elif 'height=90' in src:
                    iframe['width'] = iframe.get('width', '330')
                    iframe['height'] = iframe.get('height', '110')
                iframe['frameborder'] = iframe.get('frameborder', 'no')
                iframe['border'] = iframe.get('border', '0')
            # 处理腾讯视频嵌入
            elif re.match(r'https?://v\.qq\.com/txp/iframe/player\.html\?vid=.*', src):
                iframe['width'] = iframe.get('width', '640')
                iframe['height'] = iframe.get('height', '360')
                iframe['frameborder'] = iframe.get('frameborder', '0')
                iframe['allowfullscreen'] = iframe.get('allowfullscreen', 'true')
            # 处理 YouTube 嵌入
            elif re.match(r'https?://www\.youtube\.com/embed/.*', src) or re.match(r'https?://www\.youtube-nocookie\.com/embed/.*', src):
                iframe['width'] = iframe.get('width', '560')
                iframe['height'] = iframe.get('height', '315')
                iframe['frameborder'] = iframe.get('frameborder', '0')
                iframe['allow'] = iframe.get('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture')
                iframe['referrerpolicy'] = iframe.get('referrerpolicy', 'strict-origin-when-cross-origin')
                iframe['allowfullscreen'] = iframe.get('allowfullscreen', 'true')
            else:
                iframe.decompose()

    # 处理 TikTok 嵌入代码
    for blockquote in soup.find_all('blockquote', class_='tiktok-embed'):
        # 添加样式
        blockquote['style'] = blockquote.get('style','max-width: 605px; min-width: 325px; margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; background-color: #f9f9f9;')
        # 确保 blockquote 内的 script 标签被保留
        script_tag = soup.new_tag('script', src='https://www.tiktok.com/embed.js', async_=True)
        blockquote.append(script_tag)

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