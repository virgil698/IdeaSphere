import re
import bleach
from bs4 import BeautifulSoup
from markdown import markdown
from bleach.css_sanitizer import CSSSanitizer
import threading
from concurrent.futures import ThreadPoolExecutor

def convert_markdown_to_html(markdown_text):
    # 更新告示（banner）组件的正则表达式，避免 ReDoS 攻击
    banner_patterns = {
        'tip': r':::tip\s+([^\n]+?)\s*:::',
        'warning': r':::warning\s+([^\n]+?)\s*:::',
        'caution': r':::caution\s+([^\n]+?)\s*:::',
        'danger': r':::danger\s+([^\n]+?)\s*:::',
        'check': r':::check\s+([^\n]+?)\s*:::',
        'info': r':::info\s+([^\n]+?)\s*:::',
        'note': r':::note\s+([^\n]+?)\s*:::'
    }

    # 定义每种告示类型对应的 Font 图标（可根据需要调整）
    banner_icons = {
        'tip': 'fa-lightbulb',
        'warning': 'fa-exclamation-triangle',
        'caution': 'fa-triangle-exclamation',
        'danger': 'fa-skull',
        'check': 'fa-check-circle',
        'info': 'fa-circle-info',
        'note': 'fa-book'
    }

    # 定义告示类型对应的颜色方案
    banner_colors = {
        'tip': {'bg': '#d4edda', 'border': '#155724', 'text': '#155724', 'title': '提示'},
        'warning': {'bg': '#fff3cd', 'border': '#856404', 'text': '#856404', 'title': '警告'},
        'caution': {'bg': '#fff3cd', 'border': '#856404', 'text': '#856404', 'title': '注意'},
        'danger': {'bg': '#f8d7da', 'border': '#721c24', 'text': '#721c24', 'title': '危险'},
        'check': {'bg': '#d4edda', 'border': '#155724', 'text': '#155724', 'title': '检查'},
        'info': {'bg': '#d1ecf1', 'border': '#0c5460', 'text': '#0c5460', 'title': '信息'},
        'note': {'bg': '#e2e3e5', 'border': '#6c757d', 'text': '#6c757d', 'title': '备注'}
    }

    # 处理不带标题的告示（优化正则表达式）
    for banner_type, pattern in banner_patterns.items():
        markdown_text = re.sub(
            pattern,
            lambda m: f'<div class="banner banner-{banner_type}">' +
                      '<div class="banner-header">' +
                      f'<i class="fa {banner_icons.get(banner_type, "fa-exclamation-circle")}"></i> ' +
                      f'<h4>{banner_colors[banner_type]["title"]}</h4>' +
                      '</div>' +
                      f'<div class="banner-content">{m.group(1)}</div></div>',
            markdown_text,
            flags=re.DOTALL
        )

    # 预处理嵌套无序列表的缩进
    markdown_text = re.sub(r'(\n\s{2})(\*|\+|-)\s', r'\1    \2 ', markdown_text)

    # 启用 tables、breaks 和 fenced_code 扩展
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
    prism_autoloader_js = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js')
    prism_line_numbers_css = soup.new_tag('link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-numbers/prism-line-numbers.min.css')
    prism_line_highlight_css = soup.new_tag('link', rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/line-highlight/prism-line-highlight.min.css')
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
    soup.head.append(prism_autoloader_js)
    soup.head.append(prism_line_numbers_css)
    soup.head.append(prism_line_highlight_css)
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
            # 添加代码语言信息，如果未指定语言，则使用 'text' 作为默认语言
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
    .tiktok-embed {
        margin: 20px 0;
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 15px;
        background-color: #f9f9f9;
    }
    '''

    # 添加告示样式
    for banner_type, colors in banner_colors.items():
        style_tag.string += f'''
        .banner.banner-{banner_type} {{
            padding: 15px;
            margin-bottom: 20px;
            border: 1px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['bg']};
            color: {colors['text']};
        }}
        .banner.banner-{banner_type} .banner-header {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .banner.banner-{banner_type} .banner-header i {{
            margin-right: 10px;
            font-size: 1.2em;
        }}
        .banner.banner-{banner_type} .banner-header h4 {{
            margin: 0;
            font-size: 1em;
            font-weight: bold;
        }}
        .banner.banner-{banner_type} .banner-content {{
            margin: 0;
            word-break: break-word;
        }}
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


# 多线程优化 Markdown 解析器
class MultiThreadedMarkdownParser:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.lock = threading.Lock()
        self.cache = {}

    def parse(self, markdown_text):
        # 检查缓存
        with self.lock:
            if markdown_text in self.cache:
                return self.cache[markdown_text]

        # 提交任务到线程池
        future = self.executor.submit(convert_markdown_to_html, markdown_text)
        result = future.result()

        # 更新缓存
        with self.lock:
            self.cache[markdown_text] = result

        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown(wait=True)