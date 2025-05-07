import os
from datetime import datetime

import markdown
from flask import Blueprint, render_template

PRIVACY_FILE_NAME = 'privacy.md'
CONFIG_DIR_NAME = 'config'
OTHER_DIR_NAME = 'other'

privacy_bp = Blueprint('privacy', __name__, url_prefix='/privacy')

# 默认隐私政策内容
DEFAULT_PRIVACY_CONTENT = """
# 隐私政策

## 概述

IdeaSphere 致力于保护和尊重您的个人隐私。如果您对自己的个人信息有任何疑问，请[联系我们](/about)。

## 我们持有关于您的哪些信息

我们可能会收集以下类型的个人信息：

- 注册账户时提供的姓名、电子邮件地址等基本信息
- 使用论坛服务时生成的活动记录（如发帖、评论历史）
- 通过 Cookie 和类似技术收集的设备信息及浏览行为数据

## 如何使用您的个人信息

我们使用您的个人信息主要用于：

- 提供、维护和改进论坛服务
- 处理您的账户相关操作（如登录验证、密码重置）
- 与您沟通服务相关通知及更新
- 防范欺诈及保障服务安全

## 我们可能会以其他方式使用您的个人信息

在某些情况下，我们可能会：

- 根据法律要求或政府请求披露信息
- 在涉及合并、收购或资产出售时转移信息
- 聚合或匿名化处理数据用于统计分析和业务决策

## 确保您的数据安全

我们已实施合理的安全措施来保护您的个人信息：

- 使用加密技术传输敏感数据
- 实施访问控制限制内部人员访问权限
- 定期进行安全评估和漏洞修复

## Cookie 政策

我们使用 Cookie 和类似技术来：

- 记住您的登录状态
- 提供个性化内容推荐
- 分析网站使用情况以优化服务

您可以通过浏览器设置管理 Cookie，但可能会影响部分功能正常使用。

## 权利

您有权：

- 访问和获取您的个人信息副本
- 要求修正不准确的个人信息
- 在特定情况下请求删除个人信息
- 反对某些类型的处理（如直接营销）
- 以可移植格式接收您的数据

如需行使上述权利，请通过[联系我们](/about)页面提交请求。

## 接受本政策

使用 IdeaSphere 论坛即表示您同意本隐私政策。如不同意本政策，请不要使用我们的服务。

## 本政策的变更

我们可能会根据业务需求更新隐私政策。任何重大变更将通过站内通知或电子邮件告知您。建议您定期查阅本页面获取最新政策版本。
"""

# 获取项目根目录
project_root = os.path.abspath(os.path.dirname(__file__) + '/../../..')

# 隐私政策文件路径
PRIVACY_FILE_PATH = os.path.join(project_root, CONFIG_DIR_NAME, OTHER_DIR_NAME, PRIVACY_FILE_NAME)

# 检测并创建 config 文件夹
if not os.path.exists(os.path.join(project_root, CONFIG_DIR_NAME)):
    os.makedirs(os.path.join(project_root, CONFIG_DIR_NAME))

# 检测 config 文件夹下的 other 文件夹
other_dir_path = os.path.join(project_root, CONFIG_DIR_NAME, OTHER_DIR_NAME)
if not os.path.exists(other_dir_path):
    os.makedirs(other_dir_path)

# 检测 other 文件夹下的 privacy.md 文件
if not os.path.exists(PRIVACY_FILE_PATH):
    # 写入默认内容到 privacy.md 文件
    with open(PRIVACY_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(DEFAULT_PRIVACY_CONTENT)

# 存储隐私政策文件的最后修改时间
privacy_last_modified = None


def get_privacy_content():
    global privacy_last_modified

    # 获取当前隐私政策文件的最后修改时间
    current_last_modified = datetime.fromtimestamp(os.path.getmtime(PRIVACY_FILE_PATH))

    # 如果文件被修改过，则重新读取内容
    if privacy_last_modified is None or current_last_modified > privacy_last_modified:
        with open(PRIVACY_FILE_PATH, 'r', encoding='utf-8') as f:
            privacy_content = f.read()
        privacy_last_modified = current_last_modified
    else:
        # 如果文件未被修改，则使用之前读取的内容
        with open(PRIVACY_FILE_PATH, 'r', encoding='utf-8') as f:
            privacy_content = f.read()

    # 将 Markdown 转换为 HTML
    return markdown.markdown(privacy_content, extensions=['tables', 'fenced_code', 'meta', 'toc'])


@privacy_bp.route('/')
def privacy():
    privacy_html = get_privacy_content()
    return render_template('other/privacy.html', privacy_content=privacy_html)