import os
from datetime import datetime

import markdown
from flask import Blueprint, render_template

FAQ_FILE_NAME = 'faq.md'
CONFIG_DIR_NAME = 'config'
OTHER_DIR_NAME = 'other'

faq_bp = Blueprint('faq', __name__, url_prefix='/faq')

# 默认 FAQ 内容
DEFAULT_FAQ_CONTENT = """
**欢迎来到IdeaSphere开源社区论坛，请像对待其他任何公共平台一样尊重本论坛。我们希望通过持续的分享和交流，搭建技能、知识和兴趣的共享资源社区。**

我们欢迎每个用户在社区论坛中以健康和建设性的方式作出贡献，并且重视每个用户的参与，希望所有参与者都拥有愉快和充实的体验。以下准则旨在帮助大家将论坛打造成一个友善的场所，推动论坛文明公开的讨论。

## 鼓励有助于营造积极环境的行为：
- 尊重开源精神：尊重所参与项目的开源精神和文化，不进行任何破坏或者阻挠项目发展的行为；

- 共建共享：积极参与到讨论和贡献过程中，分享自己的经验、见解和资源，共同推动项目的发展；

- 保持友好氛围：保持友善的对话，尊重不同的观点和经验，在讨论过程中的言论保持客观、理性；

- 保持主题相关：清晰表达、紧扣主题，分享有价值的相关资源；

- 保护个人隐私：不公开其他用户的个人信息，包括但不限于电话号码、电子邮件地址、家庭住址等。

## 严禁发表包含下列内容的信息：
论坛用户享有言论自由的权利，但不得违反法律法规及政策规定，不得违反诚实信用原则及公序良俗，不得损害国家、论坛用户及第三方权利及利益，以下内容禁止在论坛发布和讨论：

- 违反宪法确定的基本原则的；

- 危害国家安全，泄露国家秘密，颠覆国家政权，破坏国家统一的；

- 损害国家荣誉和利益的；

- 煽动民族仇恨、民族歧视，破坏民族团结的；

- 破坏国家宗教政策，宣扬邪教和封建迷信的；

- 散布谣言，扰乱社会秩序，破坏社会稳定的；

- 散布淫秽、色情、赌博、暴力、恐怖或者教唆犯罪的；

- 侮辱或者诽谤他人，侵害他人合法权益的；

- 煽动非法集会、结社、游行、示威、聚众扰乱社会秩序的；

- 以非法民间组织名义活动的；

- 可能教唆他人犯罪的；

- 其他违反中华人民共和国法律、法规、政策，违反诚实信用及公序良俗，或者论坛用户认为不当及不宜传播的信息；

- 恶性灌水的帖子：

  - 连续发布大量相同内容的帖子

  - 发布大量没有意义文字图形

  - 发布广告、垃圾网站链接

  - 大量拷贝别人的内容（解决技术问题的拷贝不在此列）

  - 论坛管理员/版主及其他用户认为符合"恶性灌水"性质的帖子。

**论坛用户发表的文章、言论或其他信息仅代表其自身观点与立场，用户须承担一切因自己的行为而直接或间接导致的民事、行政或刑事法律责任。当发现不良行为时，我们鼓励其他用户进行举报或者联系管理员，感谢大家的支持与配合。**
"""

# FAQ 文件路径
project_root = os.path.abspath(os.path.dirname(__file__) + '/../../..')  # 获取项目根目录
FAQ_FILE_PATH = os.path.join(project_root, CONFIG_DIR_NAME, OTHER_DIR_NAME, FAQ_FILE_NAME)

# 检测并创建 config 文件夹
if not os.path.exists(os.path.join(project_root, CONFIG_DIR_NAME)):
    os.makedirs(os.path.join(project_root, CONFIG_DIR_NAME))

# 检测 config 文件夹下的 other 文件夹
other_dir_path = os.path.join(project_root, CONFIG_DIR_NAME, OTHER_DIR_NAME)
if not os.path.exists(other_dir_path):
    os.makedirs(other_dir_path)

# 检测 other 文件夹下的 faq.md 文件
if not os.path.exists(FAQ_FILE_PATH):
    # 写入默认内容到 faq.md 文件
    with open(FAQ_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(DEFAULT_FAQ_CONTENT)

# 存储 FAQ 文件的最后修改时间
faq_last_modified = None


def get_faq_content():
    global faq_last_modified

    # 获取当前 FAQ 文件的最后修改时间
    current_last_modified = datetime.fromtimestamp(os.path.getmtime(FAQ_FILE_PATH))

    # 如果文件被修改过，则重新读取内容
    if faq_last_modified is None or current_last_modified > faq_last_modified:
        with open(FAQ_FILE_PATH, 'r', encoding='utf-8') as f:
            faq_content = f.read()
        faq_last_modified = current_last_modified
    else:
        # 如果文件未被修改，则使用之前读取的内容
        with open(FAQ_FILE_PATH, 'r', encoding='utf-8') as f:
            faq_content = f.read()

    # 将 Markdown 转换为 HTML
    return markdown.markdown(faq_content, extensions=['tables', 'fenced_code', 'meta', 'toc'])


@faq_bp.route('/')
def faq():
    faq_html = get_faq_content()
    return render_template('other/faq.html', faq_content=faq_html)